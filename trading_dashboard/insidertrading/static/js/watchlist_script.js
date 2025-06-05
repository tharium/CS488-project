function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

function removeFromWatchlist(stockTicker) {
    if (confirm(`Remove ${stockTicker} from your watchlist?`)) {
        fetch(`/watchlist/remove/${stockTicker}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("Stock removed successfully!");
                location.reload();
            }
        })
        .catch(error => console.error("Failed to remove stock:", error));
    }
}

function setPrice(ticker, type) {
    let amount = document.getElementById(`${type}-price-${ticker}`).value.trim();

    if (!amount) {
        alert("Please enter a valid price.");
        return;
    }

    fetch(`/${type}price/add/${ticker}/${amount}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "X-CSRFToken": getCSRFToken(),
        },
        body: `symbol=${ticker}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            alert(`${type.charAt(0).toUpperCase() + type.slice(1)} price set successfully!`);
        }
    })
    .catch(error => {
        console.error(`Error adding to ${type} price list:`, error);
        alert(`Failed to add to ${type} price list.`);
    });
}

function togglePriceInput(ticker){
    let priceInput = document.getElementById(`price-inputs-${ticker}`);

    if (priceInput.style.display === "none") {
        priceInput.style.display = "inline-block";
    } else {
        priceInput.style.display = "none";
    }
}