(function() {
"use strict";

const ctx = document.getElementById('chart').getContext('2d');
const prices = document.getElementById('prices');
const form = document.getElementById('stock-form');
const feedback = document.getElementById('feedback');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Prices',
                data: []
            }
        ]
    },
    options: {
        title: {
            display: true,
            text: 'Your stock prices'
        },
        scales: {
            xAxes: [{display: false}],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Price ($)'
                }
            }]
        }
    }
});

function updateGraph() {
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    prices.value.split(',').forEach((val, i) => {
        val = val.trim();
        if(val.length == 0) return;
        chart.data.labels.push(i+1);
        chart.data.datasets[0].data.push(val);
    });
    chart.update();
}

prices.addEventListener('input', () => {
    updateGraph();
});

form.addEventListener('submit', async evt => {
    evt.preventDefault();
    const data = new FormData(form);
    feedback.style.display = 'none';
    const resp = await fetch('/predict', {
        method: 'POST',
        body: data
    });
    if(resp.ok) {
        const json = await resp.json();
        updateGraph();
        json.forEach((price, i) => {
            chart.data.labels.push(`Prediction ${i+1}`);
            chart.data.datasets[0].data.push(price);
        });
        chart.update();
    } else {
        feedback.style.display = 'block';
        feedback.textContent = `Error: ${await resp.text()}`;
    }
});
})();