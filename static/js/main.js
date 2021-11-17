((w, d) => {
  const htmlElement = d.querySelector('html');
  const iconGitHub =
    '<svg focusable="false" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1.27a11 11 0 00-3.48 21.46c.55.09.73-.28.73-.55v-1.84c-3.03.64-3.67-1.46-3.67-1.46-.55-1.29-1.28-1.65-1.28-1.65-.92-.65.1-.65.1-.65 1.1 0 1.73 1.1 1.73 1.1.92 1.65 2.57 1.2 3.21.92a2 2 0 01.64-1.47c-2.47-.27-5.04-1.19-5.04-5.5 0-1.1.46-2.1 1.2-2.84a3.76 3.76 0 010-2.93s.91-.28 3.11 1.1c1.8-.49 3.7-.49 5.5 0 2.1-1.38 3.02-1.1 3.02-1.1a3.76 3.76 0 010 2.93c.83.74 1.2 1.74 1.2 2.94 0 4.21-2.57 5.13-5.04 5.4.45.37.82.92.82 2.02v3.03c0 .27.1.64.73.55A11 11 0 0012 1.27"></path></svg>';
  const iconMoon =
    '<svg focusable="false" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 2c-1.05 0-2.05.16-3 .46 4.06 1.27 7 5.06 7 9.54 0 4.48-2.94 8.27-7 9.54.95.3 1.95.46 3 .46 5.52 0 10-4.48 10-10S14.52 2 9 2z"></path></svg>';
  const iconSun =
    '<svg focusable="false" viewBox="0 0 24 24" aria-hidden="true"><path d="m6.76 4.84-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7 1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 16.95h2V19.5h-2v2.95zm-7.45-3.91 1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z"></path></svg>';

  const injectCss = onLoad => {
    const scriptTag = d.querySelector('script');
    const link = d.createElement('link');
    link.onload = onLoad();
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = '/static/css/main.css';
    scriptTag.parentElement.appendChild(link);
  };

  const getCurrentTheme = () => {
    const storedTheme = w.localStorage.getItem('theme');
    let theme = 'light';

    if (storedTheme) {
      theme = storedTheme;
    } else {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      theme = mediaQuery.matches === true ? 'dark' : 'light';
    }

    return theme;
  };
  let theme = getCurrentTheme();

  const toggleTheme = theme => {
    w.localStorage.setItem('theme', theme);
    htmlElement.setAttribute('data-theme', theme);
  };

  const injectHtml = theme => {
    const main = d.querySelector('main');
    const nav = d.createElement('nav');

    const anchorMF = d.createElement('a');
    anchorMF.href = 'https://moviefeed.ishetaldonderdag.nl/';
    anchorMF.innerText = 'MovieFeed';

    const anchor = d.createElement('a');
    anchor.href = 'https://github.com/Ex-iT/ishetaldonderdag';
    anchor.title = 'IsHetAlDonderdag.nl op GitHub';
    anchor.innerHTML = iconGitHub;
    anchor.target = '_blank';
    anchor.rel = 'noopener noreferrer';

    const updateButton = (button, theme) => {
      button.title = button.ariaLabel = `Wissel naar ${
        theme === 'light' ? 'donker' : 'licht'
      } thema`;
      button.innerHTML = theme === 'light' ? iconMoon : iconSun;
    };

    const button = d.createElement('button');
    button.type = 'button';
    button.onclick = () => {
      theme = theme === 'light' ? 'dark' : 'light';
      updateButton(button, theme);
      toggleTheme(theme);
    };
    updateButton(button, theme);

    nav.prepend(anchor);
    nav.prepend(button);
    nav.prepend(anchorMF);

    main.parentElement.prepend(nav);
  };

  const urlSearchParams = new URLSearchParams(w.location.search);
  if (urlSearchParams.get('homescreen') !== '1') {
    injectCss(() => injectHtml(theme));
    htmlElement.setAttribute('data-theme', theme);
  }
})(window, document);
