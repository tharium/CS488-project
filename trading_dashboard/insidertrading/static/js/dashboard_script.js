
        
        // Initialize charts
        document.addEventListener('DOMContentLoaded', function() {
            const chartData = window.chartData;

            const chartLabels = chartData.labels
            const percentChanges = chartData.percent_changes

            const ctx = document.getElementById('portfolioPerformanceChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: chartLabels,
                    datasets: [{
                        label: '% Change Since Added',
                        data: percentChanges,
                        backgroundColor: percentChanges.map(p => p >= 0 ? 'rgba(46, 204, 113, 0.7)' : 'rgba(231, 76, 60, 0.7)'),
                        borderColor: percentChanges.map(p => p >= 0 ? '#27ae60' : '#c0392b'),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: { display: true, text: '% Change' }
                        }
                    }
                }
            });
        
            
            // Asset Allocation Chart
            const allocCtx = document.getElementById('assetAllocationChart').getContext('2d');
            const allocChart = new Chart(allocCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Stocks', 'Bonds', 'Cash', 'Real Estate', 'Crypto'],
                    datasets: [{
                        data: [65, 15, 10, 7, 3],
                        backgroundColor: [
                            '#3498db',
                            '#2ecc71',
                            '#f1c40f',
                            '#e74c3c',
                            '#9b59b6'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right'
                        }
                    }
                }
            });
            
             // Sparklines for watchlist
    document.querySelectorAll('.sparkline-container').forEach(function(canvas) {
        const values = JSON.parse(canvas.dataset.values);
        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array(values.length).fill(''),
                datasets: [{
                    data: values,
                    borderColor: values[0] < values[values.length-1] ? '#2ecc71' : '#e74c3c',
                    backgroundColor: 'transparent',
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                scales: {
                    x: {
                        display: false,
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: false,
                        grid: {
                            display: false
                        },
                        min: Math.min(...values) * 0.99,
                        max: Math.max(...values) * 1.01
                    }
                },
                elements: {
                    line: {
                        borderWidth: 1.5
                    },
                    point: {
                        radius: 0
                    }
                },
                animation: false
            }
        });
        });

            // Theme toggle functionality
        document.getElementById('checkbox').addEventListener('change', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
                
        // Check for saved theme preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
            document.getElementById('checkbox').checked = true;
        }

        document.getElementById("search-form").addEventListener("submit", function(e) {
            e.preventDefault();
            const query = this.querySelector("input[name='q']").value;
        
            fetch(`/search-stock/?q=${encodeURIComponent(query)}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById("search-result-container").innerHTML = html;
                attachAddStockListener(); // hook up dynamic form
            });
        });
        
        function attachAddStockListener() {
            const form = document.querySelector(".add-stock-form");
            if (!form) return;
        
            form.addEventListener("submit", function(e) {
                e.preventDefault();
                const csrf = form.querySelector("[name=csrfmiddlewaretoken]").value;
        
                fetch(form.action, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrf,
                        "X-Requested-With": "XMLHttpRequest"
                    }
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById("search-form").dispatchEvent(new Event("submit")); // refresh search
                });
            });
        }

    });

    