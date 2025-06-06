let stockChart = null;

function fetchStockPrice() {
    let symbol = document.getElementById("stock-symbol").value;
    if (!symbol) {
        alert("Please enter a stock symbol.");
        return;
    }

    fetch(`/api/stock/?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("result").innerText = "Error: " + data.error;
            } else {
                document.getElementById("result").innerText = `Stock Price of ${data.symbol}: $${data.price.toFixed(2)}`;
            }
        })
        .catch(error => {
            console.error("Error fetching stock price:", error);
            document.getElementById("result").innerText = "Failed to fetch stock price.";
        });
}

function fetchStockHistory() {
    var selectedPeriod = document.getElementById("period-select").value;
    let symbol = document.getElementById("stock-symbol").value;
    if (!symbol) {
        alert("Please enter a stock symbol.");
        return;
    }

    fetch(`/api/stock/history/?symbol=${symbol}&period=${selectedPeriod}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("result").innerText = "Error: " + data.error;
            } else {
                document.getElementById("result").innerText = `Stock History for ${symbol}:`;
                document.getElementById("watchlist-button").style.display = "block";
                displayStockChart(data.dates, data.prices, symbol)
            }
        })
        .catch(error => {
            console.error("Error fetching stock history:", error);
            document.getElementById("result").innerText = "Failed to fetch stock history.";
        });
}

function displayStockChart(dates, prices, symbol) {

    if (stockChart) {
        stockChart.destroy();
    }

    let ctx = document.getElementById("stockChart").getContext("2d");

    symbol = symbol.toUpperCase();

    stockChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [{
                label: `Price of ${symbol}`,
                data: prices,
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 2,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {display: true, text: "Date"}
                },
                y: {
                    title: {display: true, text: "Price ($)"},
                }
            }
        }
    })
}
