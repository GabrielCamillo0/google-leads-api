import stripe
from fastapi import APIRouter, HTTPException, Request, Depends
from backend.database import cursor, conn
from backend.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET

# Verificar se as chaves do Stripe estão configuradas corretamente
if not STRIPE_SECRET_KEY or not STRIPE_WEBHOOK_SECRET:
    raise ValueError("⚠️ Erro: STRIPE_SECRET_KEY ou STRIPE_WEBHOOK_SECRET não configurados no .env")

# Configuração do Stripe
stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter()

# Definir planos disponíveis
PLANOS = {
    "premium": {
        "price": 1990,  # Preço em centavos (R$19,90)
        "currency": "brl",
        "description": "Plano Premium - Acesso Ilimitado"
    }
}

@router.post("/create-checkout-session")
def create_checkout_session(plan: str, username: str):
    """Cria uma sessão de pagamento no Stripe para assinar o plano premium."""
    if plan not in PLANOS:
        raise HTTPException(status_code=400, detail="Plano inválido")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": PLANOS[plan]["currency"],
                    "product_data": {"name": PLANOS[plan]["description"]},
                    "unit_amount": PLANOS[plan]["price"]
                },
                "quantity": 1
            }],
            mode="payment",
            success_url="https://seusite.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://seusite.com/cancel",
            metadata={"username": username, "plan": plan}
        )
        return {"url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Erro no Stripe: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Recebe eventos do Stripe e ativa o plano premium do usuário após o pagamento."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Erro ao validar webhook - Assinatura inválida")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no webhook: {str(e)}")

    # Verificar se o pagamento foi concluído
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        username = session["metadata"]["username"]
        plan = session["metadata"]["plan"]

        # Atualizar o plano do usuário no banco de dados
        cursor.execute("UPDATE users SET plan = ? WHERE username = ?", (plan, username))
        conn.commit()

    return {"message": "Webhook processado com sucesso"}
