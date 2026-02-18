import { useState, useEffect } from 'react';
import './App.css';
import { TrendingUp, TrendingDown, Activity, BrainCircuit, RefreshCw, Layers } from 'lucide-react';

interface StockData {
    Symbol: string;
    Name: string;
    Price: number | string;
    Change: number | string;
    Volume: number | string;
    Description: string;
}

interface InsightData {
    content: string;
    generated_at?: string;
}

function App() {
    const [data, setData] = useState<StockData[]>([]);
    const [insights, setInsights] = useState<InsightData | null>(null);
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [dataRes, insightRes] = await Promise.all([
                fetch('/api/data'),
                fetch('/api/insights')
            ]);
            const dataJson = await dataRes.json();
            const insightJson = await insightRes.json();
            setData(dataJson);
            setInsights(insightJson);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div className="app">
            <header className="header">
                <div className="logo">
                    <BrainCircuit size={32} className="logo-icon" />
                    <h1>AI Data<span>Insight</span></h1>
                </div>
                <button onClick={fetchData} className="refresh-btn">
                    <RefreshCw size={20} className={loading ? 'spinning' : ''} />
                    Refresh
                </button>
            </header>

            <main className="container">
                {insights && (
                    <section className="insight-hero animate-fade-in">
                        <div className="section-header">
                            <Activity size={24} className="accent-icon" />
                            <h2>AI Market Analysis</h2>
                        </div>
                        <div className="glass-card insight-body">
                            <div className="insight-content">
                                {insights.content.split('\n').map((line, i) => (
                                    <p key={i}>{line}</p>
                                ))}
                            </div>
                        </div>
                    </section>
                )}

                <section className="market-section">
                    <div className="section-header">
                        <TrendingUp size={24} className="accent-icon" />
                        <h2>Trending Tickers</h2>
                    </div>

                    <div className="ticker-grid">
                        {data.map((item) => {
                            const change = parseFloat(item.Change.toString());
                            const isPositive = !isNaN(change) && change >= 0;

                            return (
                                <div key={item.Symbol} className="glass-card ticker-card animate-slide-up">
                                    <div className="ticker-header">
                                        <span className="symbol">{item.Symbol}</span>
                                        <span className={`change ${isPositive ? 'positive' : 'negative'}`}>
                                            {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                                            {item.Change}%
                                        </span>
                                    </div>
                                    <div className="ticker-name">{item.Name}</div>
                                    <div className="ticker-price">${item.Price}</div>
                                    <div className="ticker-volume">Vol: {item.Volume.toLocaleString()}</div>
                                    <div className="ticker-desc">{item.Description}</div>
                                </div>
                            );
                        })}
                    </div>
                </section>
            </main>

            <footer className="footer">
                <div className="footer-content">
                    <Layers size={20} />
                    <span>AI Data Insight Pipeline v2.0 - Hybrid UI</span>
                </div>
            </footer>
        </div>
    );
}

export default App;
