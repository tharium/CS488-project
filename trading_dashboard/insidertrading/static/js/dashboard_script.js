
        
document.addEventListener('DOMContentLoaded', function () {
    const sectorFilter = document.getElementById('sectorFilter');
    const tableRows = document.querySelectorAll('#watchlistTable tbody tr');
    
    sectorFilter.addEventListener('change', function() {
        const selectedSector = this.value;
        
        tableRows.forEach(row => {
            const rowSector = row.getAttribute('data-sector');
            if (selectedSector === '' || rowSector === selectedSector) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });

    // Portfolio Performance Bar Chart
    if (window.chartData) {
        const { labels: chartLabels, percent_changes: percentChanges } = window.chartData;

        const performanceCtx = document.getElementById('portfolioPerformanceChart')?.getContext('2d');
        if (performanceCtx) {
            new Chart(performanceCtx, {
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
        }
    }

    // Sector Pie Chart
    if (window.sectorChartData) {
        const pieData = {
            labels: window.sectorChartData.labels,
            datasets: [{
                data: window.sectorChartData.values,
                backgroundColor: [
                    '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e',
                    '#e74a3b', '#858796', '#20c9a6', '#ff6384',
                ],
                borderWidth: 1,
            }]
        };

        const pieConfig = {
            type: 'pie',
            data: pieData,
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' },
                    title: { display: true, text: 'Stocks by Sector' }
                }
            }
        };

        const pieCanvas = document.getElementById('sectorPieChart');
        if (pieCanvas) {
            new Chart(pieCanvas, pieConfig);
        }
    }

    // Sparklines
    document.querySelectorAll('.sparkline-container').forEach(function (canvas) {
        const values = JSON.parse(canvas.dataset.values);
        const ctx = canvas.getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array(values.length).fill(''),
                datasets: [{
                    data: values,
                    borderColor: values[0] < values[values.length - 1] ? '#2ecc71' : '#e74c3c',
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
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                scales: {
                    x: { display: false, grid: { display: false } },
                    y: {
                        display: false,
                        grid: { display: false },
                        min: Math.min(...values) * 0.99,
                        max: Math.max(...values) * 1.01
                    }
                },
                elements: {
                    line: { borderWidth: 1.5 },
                    point: { radius: 0 }
                },
                animation: false
            }
        });
    });

    // Theme Toggle
    const themeCheckbox = document.getElementById('checkbox');
    if (themeCheckbox) {
        themeCheckbox.addEventListener('change', function () {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });

        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
            themeCheckbox.checked = true;
        }
    }

    // Stock Search AJAX
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const query = this.querySelector("input[name='q']").value;

            fetch(`/search-stock/?q=${encodeURIComponent(query)}`, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById("search-result-container").innerHTML = html;
                attachAddStockListener();
            });
        });
    }

    function attachAddStockListener() {
    const form = document.querySelector(".add-stock-form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const csrf = form.querySelector("[name=csrfmiddlewaretoken]").value;

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "X-Requested-With": "XMLHttpRequest"
            },
            body: formData
        })
        .then(res => {
            if (res.redirected) {
                window.location.href = res.url;
                return;
            }
            return res.json();
        })
        .then(() => {
            
            document.getElementById("search-form").dispatchEvent(new Event("submit"));
        })
        .catch(err => {
            console.error("Error adding stock:", err);
        });
    });
}
});

    