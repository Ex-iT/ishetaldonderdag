(d => {
  const injectCss = (onLoad) => {
    const scriptTag = d.querySelector('script');
    const link = d.createElement('link');
    link.onload = onLoad();
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = '/static/css/main.css';
    scriptTag.parentElement.appendChild(link);
  };

  const injectHtml = () => {
    const main = d.querySelector('main');
    const nav = d.createElement('nav');
    nav.innerHTML = `<a href="https://github.com/Ex-iT/ishetaldonderdag" target="_blank" rel="noopener noreferrer">
        <svg focusable="false" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1.27a11 11 0 00-3.48 21.46c.55.09.73-.28.73-.55v-1.84c-3.03.64-3.67-1.46-3.67-1.46-.55-1.29-1.28-1.65-1.28-1.65-.92-.65.1-.65.1-.65 1.1 0 1.73 1.1 1.73 1.1.92 1.65 2.57 1.2 3.21.92a2 2 0 01.64-1.47c-2.47-.27-5.04-1.19-5.04-5.5 0-1.1.46-2.1 1.2-2.84a3.76 3.76 0 010-2.93s.91-.28 3.11 1.1c1.8-.49 3.7-.49 5.5 0 2.1-1.38 3.02-1.1 3.02-1.1a3.76 3.76 0 010 2.93c.83.74 1.2 1.74 1.2 2.94 0 4.21-2.57 5.13-5.04 5.4.45.37.82.92.82 2.02v3.03c0 .27.1.64.73.55A11 11 0 0012 1.27"></path></svg>
      </a>`;
    main.parentElement.prepend(nav);

    // @TODO: inject theme toggle button
    // <button type="button" aria-label="Wissel thema">
    //  <svg focusable="false" viewBox="0 0 24 24" aria-hidden="true"><path d="m6.76 4.84-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7 1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 16.95h2V19.5h-2v2.95zm-7.45-3.91 1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z"></path></svg>
    // </button>
  };

  injectCss(injectHtml);
})(document);
