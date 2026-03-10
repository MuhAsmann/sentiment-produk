
document.addEventListener('DOMContentLoaded', () => {
    const compareBtn = document.getElementById('compare-btn');
    const url1Input = document.getElementById('url1');
    const url2Input = document.getElementById('url2');
    const resultSection = document.getElementById('result-section');
    const loader = document.getElementById('loader');

    let charts = { p1: null, p2: null };

    compareBtn.addEventListener('click', async () => {
        const url1 = url1Input.value.trim();
        const url2 = url2Input.value.trim();

        if (!url1 || !url2) {
            alert('Silakan masukkan kedua URL produk Tokopedia!');
            return;
        }

        loader.classList.remove('hidden');
        resultSection.classList.add('hidden');

        try {
            const response = await fetch('/compare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url1, url2 })
            });

            const data = await response.json();

            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            renderResults(data);
        } catch (error) {
            console.error('Error fetching dynamic comparison:', error);
            alert('Terjadi kesalahan saat menghubungi server.');
        } finally {
            loader.classList.add('hidden');
        }
    });

    function renderResults(data) {
        const { product1, product2, comparison } = data;

        // Product 1
        document.getElementById('p1-name').textContent = product1.productName;
        document.getElementById('p1-shop').textContent = product1.shopName;
        document.getElementById('p1-rating').textContent = product1.rating;
        document.getElementById('p1-pos').textContent = product1.sentiment.positive_pct + '%';
        document.getElementById('p1-neu').textContent = product1.sentiment.neutral_pct + '%';
        document.getElementById('p1-neg').textContent = product1.sentiment.negative_pct + '%';

        // Product 2
        document.getElementById('p2-name').textContent = product2.productName;
        document.getElementById('p2-shop').textContent = product2.shopName;
        document.getElementById('p2-rating').textContent = product2.rating;
        document.getElementById('p2-pos').textContent = product2.sentiment.positive_pct + '%';
        document.getElementById('p2-neu').textContent = product2.sentiment.neutral_pct + '%';
        document.getElementById('p2-neg').textContent = product2.sentiment.negative_pct + '%';

        const winnerBadge = document.getElementById('winner-badge');
        winnerBadge.textContent = '🏅 ' + comparison.winner + ' Menang!';

        const summaryText = document.getElementById('summary-text');
        summaryText.innerHTML = `Berdasarkan analisis sentimen dari komentar pembeli, <strong>${comparison.winner}</strong> memiliki skor kepuasan yang lebih tinggi. Perbedaan skor rata-rata adalah <strong>${comparison.score_diff}</strong> poin.`;

        // Render Charts
        renderChart('p1-chart', product1.sentiment, 'p1');
        renderChart('p2-chart', product2.sentiment, 'p2');

        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    function renderChart(containerId, sentiment, key) {
        const options = {
            series: [sentiment.positive_pct, sentiment.neutral_pct, sentiment.negative_pct],
            chart: {
                type: 'donut',
                height: 300,
                background: 'transparent'
            },
            labels: ['Positif', 'Netral', 'Negatif'],
            colors: ['#10b981', '#f59e0b', '#ef4444'],
            dataLabels: { enabled: false },
            legend: { position: 'bottom', labels: { colors: '#94a3b8' } },
            stroke: { show: false },
            theme: { mode: 'dark' },
            plotOptions: {
                pie: {
                    donut: {
                        size: '75%',
                        labels: {
                            show: true,
                            total: {
                                show: true,
                                label: 'Rata-rata',
                                formatter: () => sentiment.average,
                                color: '#f8fafc'
                            }
                        }
                    }
                }
            }
        };

        if (charts[key]) {
            charts[key].destroy();
        }

        charts[key] = new ApexCharts(document.getElementById(containerId), options);
        charts[key].render();
    }
});
