var stockChart = null;

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

function fetchStockHistory(){
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
                borderColor: "rgb(62, 187, 79)",
                borderWidth: 2,
                pointBorderWidth: 1,
                pointRadius: 1,
                fill: false,
            }]
        }
    });
}

function addToWatchlist(){
    let symbol = document.getElementById("stock-symbol").value.trim().toUpperCase();
    
    if (!symbol) {
        alert("Please fetch stock data first.");
        return;
    }

    fetch(`/watchlist/add/${symbol}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "X-CSRFToken": getCSRFToken(),
        },
        body: `symbol=${symbol}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            alert("Added to watchlist successfully!");
        }
    })
    .catch(error => {
        console.error("Error adding to watchlist:", error);
        alert("Failed to add to watchlist.");
    });
}

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

