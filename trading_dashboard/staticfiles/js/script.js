function fetchStockPrice() {
    let symbol = document.getElementById("stock-symbol").value.trim().toUpperCase();

    if (!symbol) {
        alert("Please enter a stock symbol.");
        return;
    }

    fetch(`/api/stock/?symbol=${symbol}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                document.getElementById("result").innerHTML = `<span style="color:red;">Error: ${data.error}</span>`;
            } else {
                document.getElementById("result").innerHTML = `<strong>Stock Price of ${data.symbol}:</strong> $${parseFloat(data.price).toFixed(2)}`;
            }
        })
        .catch(error => {
            console.error("Error fetching stock price:", error);
            document.getElementById("result").innerHTML = `<span style="color:red;">Failed to fetch stock price.</span>`;
        });
}
