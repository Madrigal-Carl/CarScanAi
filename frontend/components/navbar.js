class CustomNavbar extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        nav {
          background: rgba(17, 24, 39, 0.9);
          backdrop-filter: blur(8px);
          padding: 1rem 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          position: fixed;
          width: 100%;
          top: 0;
          z-index: 50;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .logo {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1.25rem;
          font-weight: bold;
          color: white;
        }
        .logo svg {
          color: #3B82F6;
        }
        ul {
          display: none;
        }
        button {
          background: #3B82F6;
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 9999px;
          font-weight: 500;
          transition: all 0.2s;
        }
        button:hover {
          background: #2563EB;
        }
        @media (min-width: 768px) {
          ul {
            display: flex;
            gap: 2rem;
            list-style: none;
          }
          a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: color 0.2s;
            font-weight: 500;
          }
          a:hover {
            color: #3B82F6;
          }
        }
      </style>
      <nav>
        <div class="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
          </svg>
          <span>CarVision<span style="color: #3B82F6">AI</span></span>
        </div>
        <ul>
          <li><a href="#features">Features</a></li>
          <li><a href="#how-it-works">How It Works</a></li>
          <li><a href="#demo">Demo</a></li>
        </ul>
        <button>
          Try Now
        </button>
      </nav>
    `;
    feather.replace();
  }
}
customElements.define('custom-navbar', CustomNavbar);