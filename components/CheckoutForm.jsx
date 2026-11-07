import React, { useState } from 'react';

export default function CheckoutForm() {
  const [playerId, setPlayerId] = useState('');
  const [zoneId, setZoneId] = useState('');
  const [productCode, setProductCode] = useState('wild_core_500'); // default sample code
  const [loading, setLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState(null);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponseMessage(null);

    try {
      // Calls your live Render backend API endpoint
      const response = await fetch('https://wildcore-api.onrender.com/api/create-order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          player_id: playerId,
          zone_id: zoneId,
          product_code: productCode,
        }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setIsSuccess(true);
        setResponseMessage('Top-up order successfully processed and fulfilled!');
      } else {
        setIsSuccess(false);
        setResponseMessage(data.detail || 'Failed to process order. Please check your IDs.');
      }
    } catch (error) {
      setIsSuccess(false);
      setResponseMessage('Network error connecting to payment/order server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-slate-900 text-white p-6 rounded-xl shadow-2xl border border-slate-800">
      <h2 className="text-2xl font-bold mb-6 text-center text-indigo-400">Instant Game Top-Up</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Player ID Input */}
        <div>
          <label className="block text-sm font-medium mb-1 text-slate-300">Player ID</label>
          <input
            type="text"
            required
            value={playerId}
            onChange={(e) => setPlayerId(e.target.value)}
            placeholder="Enter your Game ID"
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500"
          />
        </div>

        {/* Zone ID Input */}
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

        {/* Product Selection */}
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

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 rounded-lg transition duration-200 disabled:opacity-50"
        >
          {loading ? 'Processing Order...' : 'Proceed to Checkout'}
        </button>
      </form>

      {/* Response Message */}
      {responseMessage && (
        <div className={`mt-4 p-3 rounded-lg text-sm ${isSuccess ? 'bg-emerald-900/50 text-emerald-300 border border-emerald-700' : 'bg-rose-900/50 text-rose-300 border border-rose-700'}`}>
          {responseMessage}
        </div>
      )}
    </div>
  );
}