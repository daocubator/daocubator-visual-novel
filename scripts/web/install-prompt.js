// "Install — to play fullscreen" button for the Ren'Py web build.
// Injected into web-build/index.html by scripts/patch_web_build.py.
//
// Shown only on phones/tablets, and only when not already running as an
// installed app. On Chrome/Edge/Samsung (Android) it fires the native install
// prompt; elsewhere (iOS Safari, or before Chrome offers the prompt) it shows
// short manual instructions instead.
(function () {
  var standalone =
    window.matchMedia('(display-mode: standalone)').matches ||
    window.matchMedia('(display-mode: fullscreen)').matches ||
    window.navigator.standalone === true;
  if (standalone) return;

  var ua = navigator.userAgent || '';
  var isIOS = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  var isMobile =
    (navigator.userAgentData && navigator.userAgentData.mobile) ||
    isIOS || /Android|Mobi/i.test(ua) ||
    (window.matchMedia('(pointer: coarse)').matches && Math.min(screen.width, screen.height) < 820);
  if (!isMobile) return;

  var DISMISS_KEY = 'grt-install-dismissed';
  try { if (localStorage.getItem(DISMISS_KEY)) return; } catch (e) {}

  var deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferredPrompt = e;
  });

  var css = document.createElement('style');
  css.textContent = [
    '#grtInstall{position:fixed;top:max(10px,env(safe-area-inset-top));right:max(10px,env(safe-area-inset-right));z-index:1000;',
    'display:flex;align-items:stretch;font-family:Georgia,"Times New Roman",serif;',
    'background:rgba(28,22,16,.92);border:1px solid #b8964f;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.5);',
    'color:#e8d6a8;-webkit-user-select:none;user-select:none;touch-action:manipulation}',
    '#grtInstall button{font:inherit;color:inherit;background:none;border:0;cursor:pointer;-webkit-tap-highlight-color:transparent}',
    '#grtInstallBtn{display:flex;flex-direction:column;align-items:flex-start;gap:1px;padding:8px 6px 8px 14px;text-align:left}',
    '#grtInstallBtn b{font-size:15px;letter-spacing:.08em;text-transform:uppercase;color:#f0c96a}',
    '#grtInstallBtn span{font-size:11px;opacity:.8}',
    '#grtInstallX{padding:0 12px;font-size:18px;opacity:.6;border-left:1px solid rgba(184,150,79,.35)!important}',
    '#grtInstallHelp{position:fixed;inset:0;z-index:1001;display:flex;align-items:center;justify-content:center;',
    'background:rgba(0,0,0,.6);font-family:Georgia,serif}',
    '#grtInstallHelp>div{max-width:320px;margin:16px;padding:18px 20px;background:#1c1610;border:1px solid #b8964f;',
    'border-radius:10px;color:#e8d6a8;font-size:15px;line-height:1.45}',
    '#grtInstallHelp b{color:#f0c96a}',
    '#grtInstallHelp button{margin-top:14px;font:inherit;color:#1c1610;background:#f0c96a;border:0;border-radius:6px;padding:8px 16px}'
  ].join('');
  document.head.appendChild(css);

  var bar = document.createElement('div');
  bar.id = 'grtInstall';
  bar.innerHTML =
    '<button id="grtInstallBtn" type="button"><b>Install</b><span>to play fullscreen</span></button>' +
    '<button id="grtInstallX" type="button" aria-label="Dismiss">&times;</button>';

  function hide() { if (bar.parentNode) bar.parentNode.removeChild(bar); }

  function showHelp() {
    var steps = isIOS
      ? 'Tap the <b>Share</b> button in Safari, then <b>Add to Home Screen</b>.'
      : 'Open the browser menu (<b>&#8942;</b>), then tap <b>Install app</b> or <b>Add to Home screen</b>.';
    var help = document.createElement('div');
    help.id = 'grtInstallHelp';
    help.innerHTML = '<div>' + steps + '<br>Launch the game from the new icon to play fullscreen.' +
      '<br><button type="button">Got it</button></div>';
    help.addEventListener('click', function () { help.parentNode.removeChild(help); });
    document.body.appendChild(help);
  }

  // Keep taps on the button from reaching the Ren'Py canvas.
  ['pointerdown', 'mousedown', 'touchstart', 'touchend', 'mouseup', 'pointerup'].forEach(function (t) {
    bar.addEventListener(t, function (e) { e.stopPropagation(); }, { passive: true });
  });

  bar.querySelector('#grtInstallBtn').addEventListener('click', function () {
    if (!deferredPrompt) return showHelp();
    var p = deferredPrompt;
    deferredPrompt = null;
    p.prompt();
    p.userChoice.then(function (c) { if (c && c.outcome === 'accepted') hide(); });
  });

  bar.querySelector('#grtInstallX').addEventListener('click', function () {
    try { localStorage.setItem(DISMISS_KEY, '1'); } catch (e) {}
    hide();
  });

  window.addEventListener('appinstalled', hide);

  if (document.body) document.body.appendChild(bar);
  else document.addEventListener('DOMContentLoaded', function () { document.body.appendChild(bar); });
})();
