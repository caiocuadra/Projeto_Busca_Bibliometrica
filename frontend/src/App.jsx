// frontend/src/App.jsx
import { useState } from 'react';
import './index.css'; // Garante que os estilos sejam carregados

function App() {
  const [query, setQuery] = useState('');
  
  // Dados simulados para visualizar a interface (Mock Data)
  const mockResults = [
    {
      id: 1,
      title: "Natural Language Processing in Bibliometric Analysis: A Review",
      authors: "Silva, J. & Santos, M.",
      year: 2024,
      journal: "Journal of Data Science",
      abstract: "This paper explores the application of Sentence-BERT and other NLP techniques to improve the relevance ranking of academic search results...",
      citations: 45
    },
    {
      id: 2,
      title: "Optimizing Academic Search Engines using Machine Learning",
      authors: "Cuadra, C. H. M. & Souza, E. M. B.",
      year: 2025,
      journal: "Future Tech Symposium",
      abstract: "Addressing the noise in academic literature search through automated refinement and semantic ranking algorithms.",
      citations: 12
    },
    {
      id: 3,
      title: "The Future of Scientometrics",
      authors: "Doe, A. et al.",
      year: 2023,
      journal: "Scientometrics Today",
      abstract: "An overview of how AI agents are reshaping the way researchers discover and consume scientific knowledge.",
      citations: 89
    }
  ];

  const handleSearch = (e) => {
    e.preventDefault();
    alert(`Buscando por: ${query} (Conexão com backend pendente)`);
  };

  return (
    <div className="app-container">
      {/* Cabeçalho */}
      <header>
        <h1>Busca Bibliométrica Inteligente</h1>
        <nav>
          {/* Espaço para menu futuro: Login, Sobre, etc. */}
        </nav>
      </header>

      {/* Área de Busca Principal */}
      <main>
        <section className="search-section">
          <h2>Busca Bibliométrica Inteligente</h2>
          <p>Encontre artigos relevantes com ranqueamento semântico e refinamento automático.</p>
          
          <form className="search-box" onSubmit={handleSearch}>
            <input 
              type="text" 
              className="search-input"
              placeholder="Ex: processamento de linguagem natural em saúde..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button type="button" className="btn-primary" onClick={handleSearch}>
              Pesquisar
            </button>
          </form>
        </section>

        {/* Lista de Resultados */}
        <section className="results-section">
          <div className="results-header">
            <span className="results-count">Mostrando 3 de 1.240 resultados</span>
            
            <div className="export-actions">
              {/* Botões conforme Escopo do MVP: CSV e PDF */}
              <button className="btn-secondary" title="Exportar tabela">
                📥 CSV
              </button>
              <button className="btn-secondary" title="Gerar Relatório">
                📄 Relatório PDF
              </button>
            </div>
          </div>

          <div className="results-list">
            {mockResults.map((paper) => (
              <article key={paper.id} className="paper-card">
                <a href="#" className="paper-title">{paper.title}</a>
                <div className="paper-meta">
                  <span>{paper.authors}</span> • <span>{paper.year}</span> • <span>{paper.journal}</span>
                </div>
                <p className="paper-abstract">
                  {paper.abstract}
                </p>
                <div className="paper-tags">
                  <span className="tag">Citações: {paper.citations}</span>
                  <span className="tag">Relevância: Alta</span>
                </div>
              </article>
            ))}
          </div>
        </section>
      </main>

      {/* Rodapé */}
      <footer>
        <p>&copy; 2025 Sociedade Busca Bibliométrica Inteligente. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}

export default App;