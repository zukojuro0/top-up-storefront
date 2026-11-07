import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

GAMESDROP_API_KEY = os.getenv("GAMESDROP_API_KEY")
GAMESDROP_BASE_URL = "https://partner.gamesdrop.io"

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
              const res = await fetch(`/api/create-order?player_id=${encodeURIComponent(playerId)}&zone_id=${encodeURIComponent(zoneId)}&product_code=${encodeURIComponent(productCode)}`, {
                method: 'POST'
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
                    value={playerId