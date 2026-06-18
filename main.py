import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import razorpay
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


KEY_ID = os.getenv("RAZORPAY_API_KEY")
KEY_SECRET = os.getenv("RAZORPAY_API_KEY_SECRET")

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

@app.get("/", response_class=HTMLResponse)
async def checkout_page():
    amount_in_paise = 50000

    try:
        order = client.order.create(
            {
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1
            }
        )
        order_id = order['id']
    except Exception as e:
        return f"<h2>Error generating razorpay order token:{str(e)}</h2>"
    
    return f"""
    <html>
      <head>
        <title>Razorpay FastAPI Sandbox</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
      </head>
      <body style="text-align:center; margin-top:100px; font-family:-apple-system, BlinkMacSystemFont, sans-serif;">
        <div style="max-width: 400px; margin: 0 auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <h2>Checkout</h2>
            <p style="color: #666;">Testing Sandbox Payments</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 30px;">₹500.00</p>
            
            <button id="rzp-button" style="width: 100%; padding: 12px; font-size: 16px; background:#3399cc; color:white; border:none; border-radius:5px; cursor:pointer; font-weight: bold;">
                Pay Now
            </button>
        </div>

        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        <script>
        var options = {{
            "key": "{KEY_ID}",
            "amount": "{amount_in_paise}",
            "currency": "INR",
            "name": "FastAPI Sandbox Environment",
            "description": "Zero Rupee Development",
            "order_id": "{order_id}",
            "callback_url": "http://localhost:8000/verify-payment",
            "theme": {{
                "color": "#3399cc"
            }}
        }};
        var rzp1 = new Razorpay(options);
        document.getElementById('rzp-button').onclick = function(e){{
            rzp1.open();
            e.preventDefault();
        }}
        </script>
      </body>
    </html>
    """

@app.post('/verify-payment')
async def verify_payment(
    razorpay_payment_id:str = Form(...),
    razorpay_order_id:str = Form(...),
    razorpay_signature:str = Form(...)
):
    try:
        client.utility.verify_payment_signature(
            {
                'razorpay_order_id':razorpay_order_id,
                'razorpay_payment_id':razorpay_payment_id,
                'razorpay_signature':razorpay_signature
            }
        )

        return{
            "status": "success",
            "message":"Payment verified securely",
            "details":{
                "order_id":razorpay_order_id,
                "payment_id":razorpay_payment_id
            }
        }
    except razorpay.errors.SignatureVerificationError:
        return {
            "status":"error",
            "message":"Cryptographic signature verification failed"
        }