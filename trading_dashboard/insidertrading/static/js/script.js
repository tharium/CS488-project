var stockChart = null;

if (typeof isAuthenticated !== 'undefined' && isAuthenticated) {
    const loginBtn = document.getElementById('login-button');
    const signupBtn = document.getElementById('signup-button');
    if (loginBtn) {
        loginBtn.textContent = 'Logout';
        loginBtn.href = '/logout/';
    }
    if (signupBtn) {
        signupBtn.classList.add('hidden');
    }
}

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

class LiveTicker {
    constructor(containerId = 'ticker-bar', updateInterval = 600000) { // calls every 10 mins instead of 5 mins
        this.container = document.getElementById(containerId);
        this.updateInterval = updateInterval;
        this.isLoading = false;
        this.tickerData = [];

        if (!this.container) {
            console.error(`Ticker container with ID '${containerId}' not found`);
            return;
        }

        this.init();
    }

    init() {
        this.showLoadingState();
        this.fetchTickerData();

        // Set up periodic updates
        setInterval(() => {
            if (!this.isLoading) {
                this.fetchTickerData();
            }
        }, this.updateInterval);
    }

    showLoadingState() {
        this.container.innerHTML = `
            <div class="loading-ticker">
            <span>Loading market data...</span>
            </div>
        `;
    }

    async fetchTickerData() {
        this.isLoading = true;

        try {
            const response = await fetch('/api/tickers/');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this.tickerData = data;
            this.updateTickerDisplay();
        } catch (error) {
            console.error('Error fetching ticker data:', error);
            this.showErrorState();
        } finally {
            this.isLoading = false;
        }
    }

    updateTickerDisplay() {
        if (!this.tickerData || this.tickerData.length === 0) {
            this.showErrorState();
            return;
        }

        const tickerHTML = this.tickerData
            .map((stock) => {
                const changeClass = stock.change_pct >= 0 ? 'positive' : 'negative';
                const changeSymbol = stock.change_pct >= 0 ? '+' : '';
                return `
                <div class="ticker-item" data-symbol="${stock.symbol}">
                <span class="ticker-symbol">${stock.symbol}</span>
                <span class="ticker-price">$${this.formatPrice(stock.price)}</span>
                <span class="ticker-change ${changeClass}">
                    ${changeSymbol}${stock.change_pct.toFixed(2)}%
                </span>
                </div>
            `;
            })
            .join('');

        this.container.innerHTML = tickerHTML;
        this.addClickHandlers();
    }

    formatPrice(price) {
        if (price === 0 || price === null || price === undefined) {
            return '0.00';
        }
        if (price >= 1000) {
            return price.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
            });
        } else {
            return price.toFixed(2);
        }
    }

    showErrorState() {
        this.container.innerHTML = `
            <div class="loading-ticker" style="color: #ef4444;">
            <span>Unable to load market data. Retrying...</span>
            </div>
        `;
    }

    addClickHandlers() {
        const tickerItems = this.container.querySelectorAll('.ticker-item');
        tickerItems.forEach((item) => {
            item.style.cursor = 'pointer';
            item.addEventListener('click', () => {
                const symbol = item.dataset.symbol;
                console.log(`Clicked on ${symbol}`);
                // e.g. window.location.href = `/stock/${symbol}/`;
            });
        });
    }

    refresh() {
        if (!this.isLoading) {
            this.fetchTickerData();
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('ticker-bar')) {
        const ticker = new LiveTicker('ticker-bar', 30000);
        window.liveTicker = ticker;
        window.addEventListener('focus', () => {
            ticker.refresh();
        });
    }
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

                    anchor.addEventListener('click', function (e) {

                        e.preventDefault();

                        document.querySelector(this.getAttribute('href')).scrollIntoView({

                            behavior: 'smooth'

                        });

                    });

                });

