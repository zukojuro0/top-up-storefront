import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

GAMESDROP_API_KEY = os.getenv("GAMESDROP_API_KEY")
GAMESDROP_BASE_URL = "https://partner.gamesdrop.io"

class OrderRequest(BaseModel):
    player_id: str
    zone_id: str
    product_code: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>WildCore Top-Up Store</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
      <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
      <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    </head>
    <body class="bg-slate-950 text-white min-h-screen flex items-center justify-center p-4">
      <div id="root"></div>

      <script type="text/babel">
        function App() {
          const [playerId, setPlayerId] = React.useState('');
          const [zoneId, setZoneId] = React.useState('');
          const [productCode, setProductCode] = React.useState('wild_core_500');
          const [loading, setLoading] = React.useState(false);
          const [responseMessage, setResponseMessage] = React.useState(null);
          const [isSuccess, setIsSuccess] = React.useState(false);

          const handleSubmit = async (e) => {
            e.preventDefault();
            setLoading(true);
            setResponseMessage(null);

            try {
              const res = await fetch('/api/create-order', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                  player_id: playerId,
                  zone_id: zoneId,
                  product_code: productCode
                })
              });

              const data = await res.json();

              if (res.ok && data.success) {
                setIsSuccess(true);
                setResponseMessage('Top-up order successfully processed!');
              } else {
                setIsSuccess(false);
                setResponseMessage(data.detail || 'Failed to process order.');
              }
            } catch (err) {
              setIsSuccess(false);
              setResponseMessage('Network error connecting to payment/order server.');
            } finally {
              setLoading(false);
            }
          };

          return (
            <div className="max-w-md w-full bg-slate-900 p-6 rounded-xl shadow-2xl border border-slate-800">
              <h2 className="text-2xl font-bold mb-6 text-center text-indigo-400">WildCore Top-Up Store</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1 text-slate-300">Player ID</label>
                  <input
                    type="text"
                    required
                    value={playerId}
                    onChange={(e) => setPlayerId(e.target.value)}
                    placeholder="Enter Game ID"
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1 text-slate-300">Zone ID / Server ID</label>
                  <input
                    type="text"
                    required
                    value={zoneId}
                    onChange={(e) => setZoneId(e.target.value)}
                    placeholder="Enter Zone ID (e.g. 1234)"
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1 text-slate-300">Select Package</label>
                  <select
                    value={productCode}
                    onChange={(e) => setProductCode(e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500"
                  >
                    <option value="wild_core_500">Wild Rift: 500 Wild Cores</option>
                    <option value="wild_core_1000">Wild Rift: 1,000 Wild Cores</option>
                    <option value="ml_diamonds_500">Mobile Legends: 500 Diamonds</option>
                    <option value="ml_diamonds_1000">Mobile Legends: 1,000 Diamonds</option>
                  </select>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 rounded-lg transition duration-200 disabled:opacity-50"
                >
                  {loading ? 'Processing Order...' : 'Proceed to Checkout'}
                </button>
              </form>

              {responseMessage && (
                <div className={`mt-4 p-3 rounded-lg text-sm ${isSuccess ? 'bg-emerald-900/50 text-emerald-300 border border-emerald-700' : 'bg-rose-900/50 text-rose-300 border border-rose-700'}`}>
                  {responseMessage}
                </div>
              )}
            </div>
          );
        }

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
      </script>
    </body>
    </html>
    """

@app.post("/api/create-order")
def create_order(order: OrderRequest):
    headers = {
        "Authorization": f"Bearer {GAMESDROP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "product_code": order.product_code,
        "player_id": order.player_id,
        "zone_id": order.zone_id
    }
    
    try:
        response = requests.post(f"{GAMESDROP_BASE_URL}/v1/orders", json=payload, headers=headers)
        
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=response.json())
            
        return {
            "success": True,
            "message": "Order successfully processed by GamesDrop!",
            "supplier_response": response.json()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))