# Razorpay Payment Gateway Integration with FastAPI

A production-ready Razorpay payment gateway integration built using **FastAPI**, **UV**, and **Uvicorn**. This project demonstrates creating payment orders, verifying payment signatures, and handling successful payments securely.

---

## 🚀 Features

- FastAPI-based REST API
- Razorpay Order Creation
- Payment Signature Verification
- Environment Variable Configuration
- Async API Support
- UV Package Manager Support
- Uvicorn ASGI Server
- Production-Ready Structure

---

## 🛠 Tech Stack

- FastAPI
- Razorpay Python SDK
- UV
- Uvicorn
- Python 3.11+
- Pydantic
- Python Dotenv

---

## 📂 Project Structure

```text
razorpay-fastapi/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   │   └── payment.py
│   ├── services/
│   │   └── razorpay_service.py
│   └── schemas/
│       └── payment.py
│
├── .env
├── pyproject.toml
├── uv.lock
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/razorpay-fastapi.git
cd razorpay-fastapi
```

### 2. Create Virtual Environment

Using UV:

```bash
uv venv
```

Activate Environment:

#### Linux/macOS

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv pip install fastapi uvicorn razorpay python-dotenv
```

Or

```bash
uv sync
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxx
```

---

## ▶️ Running the Application

Development Server:

```bash
uv run uvicorn app.main:app --reload
```

Or

```bash
uvicorn app.main:app --reload
```

Server URL:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 📡 API Endpoints

### Health Check

#### Request

```http
GET /
```

#### Response

```json
{
  "message": "API is running"
}
```

---

### Create Order

#### Request

```http
POST /payment/create-order
```

#### Body

```json
{
  "amount": 500
}
```

> Amount is in INR. Razorpay automatically converts it to paise.

#### Response

```json
{
  "id": "order_Q123456789",
  "amount": 50000,
  "currency": "INR",
  "status": "created"
}
```

---

### Verify Payment

#### Request

```http
POST /payment/verify
```

#### Body

```json
{
  "razorpay_order_id": "order_Q123456789",
  "razorpay_payment_id": "pay_Q123456789",
  "razorpay_signature": "generated_signature"
}
```

#### Success Response

```json
{
  "success": true,
  "message": "Payment verified successfully"
}
```

#### Failure Response

```json
{
  "success": false,
  "message": "Invalid payment signature"
}
```

---

## 💳 Razorpay Checkout Example

```html
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>

<script>
const options = {
    key: "YOUR_KEY_ID",
    amount: order.amount,
    currency: "INR",
    name: "Your Company",
    description: "Test Transaction",
    order_id: order.id,

    handler: function(response) {
        console.log(response);
    }
};

const rzp = new Razorpay(options);
rzp.open();
</script>
```

---

## 🧩 FastAPI Integration Example

### Initialize Razorpay Client

```python
import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)
```

### Create Order

```python
order = client.order.create({
    "amount": amount * 100,
    "currency": "INR",
    "payment_capture": 1
})
```

### Verify Payment Signature

```python
client.utility.verify_payment_signature({
    "razorpay_order_id": razorpay_order_id,
    "razorpay_payment_id": razorpay_payment_id,
    "razorpay_signature": razorpay_signature
})
```

---

## 🧪 Testing

Use Razorpay Test Mode credentials.

### Test Card Details

```text
Card Number : 4111 1111 1111 1111
Expiry Date : Any Future Date
CVV         : Any 3 Digits
OTP         : 123456
```

---

## 🔔 Webhook Support

Create a webhook endpoint:

```http
POST /payment/webhook
```

Recommended Events:

```text
payment.authorized
payment.captured
payment.failed
order.paid
refund.processed
```

Always verify the webhook signature before processing events.

---

## 🔒 Security Best Practices

- Never expose your Razorpay Secret Key.
- Verify all payment signatures.
- Use HTTPS in production.
- Validate request payloads.
- Store payment records in a database.
- Implement proper logging and monitoring.
- Verify webhook signatures.
- Use environment variables for secrets.

---

## 🚀 Production Deployment

Install Gunicorn:

```bash
uv pip install gunicorn
```

Run:

```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Your Name**

- GitHub: https://github.com/your-username
- Email: your-email@example.com

---

## 🙏 Acknowledgements

- FastAPI
- Razorpay
- Uvicorn
- UV Package Manager

---

⭐ If you found this project useful, please consider giving it a star on GitHub.