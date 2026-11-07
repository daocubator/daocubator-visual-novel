/* @ds-bundle: {"format":4,"namespace":"DAOcubator","components":[{"name":"Panel"},{"name":"HungPanel"},{"name":"NodeCard"},{"name":"ComparisonTable"},{"name":"PullQuote"}]} */
(function () {
  var h = window.React.createElement;
  function cx() { return Array.prototype.filter.call(arguments, Boolean).join(' '); }

  function Panel(p) {
    return h('section', { className: cx('dc-panel', p.tone === 'deep' && 'dc-panel--deep', p.framed && 'dc-panel--framed', p.className) },
      p.title ? h('h3', { className: 'dc-panel__title' }, p.title) : null,
      h('div', { className: 'dc-panel__body' }, p.children));
  }

  function HungPanel(p) {
    return h('div', { className: cx('dc-hung', p.className) },
      h('div', { className: 'dc-hung__frame' },
        h('div', { className: 'dc-hung__wall' },
          h('span', { className: 'dc-hung__tie dc-hung__tie--a', 'aria-hidden': 'true' }),
          h('span', { className: 'dc-hung__tie dc-hung__tie--b', 'aria-hidden': 'true' }),
          h('section', { className: 'dc-hung__panel' },
            p.title ? h('h3', { className: 'dc-panel__title' }, p.title) : null,
            h('div', { className: 'dc-panel__body' }, p.children)),
          h('span', { className: 'dc-hung__tail dc-hung__tail--a', 'aria-hidden': 'true' }),
          h('span', { className: 'dc-hung__tail dc-hung__tail--b', 'aria-hidden': 'true' }))));
  }

  function NodeCard(p) {
    return h('div', { className: cx('dc-node', p.side === 'right' && 'dc-node--right', p.className) },
      h('div', { className: 'dc-ring', 'aria-hidden': 'true' }, p.icon || null),
      h('div', { className: 'dc-node__card' },
        p.label ? h('p', { className: 'dc-node__label' }, p.label) : null,
        h('p', { className: 'dc-node__body' }, p.children)));
  }

  function ComparisonTable(p) {
    var cols = p.columns || [], rows = p.rows || [];
    return h('table', { className: cx('dc-table', p.className) },
      h('thead', null, h('tr', null,
        h('th', { scope: 'col' }, p.corner || ''),
        cols.map(function (c, i) { return h('th', { key: i, scope: 'col' }, c); }))),
      h('tbody', null, rows.map(function (r, i) {
        return h('tr', { key: i },
          h('th', { scope: 'row' }, r.label),
          (r.cells || []).map(function (c, j) { return h('td', { key: j }, c); }));
      })));
  }

  function PullQuote(p) {
    return h('figure', { className: cx('dc-quote', p.className), style: { margin: 0 } },
      p.lede ? h('p', { className: 'dc-quote__lede' }, p.lede, p.emphasis ? h('br') : null, p.emphasis ? h('strong', null, p.emphasis) : null) : null,
      p.body ? h('p', { className: 'dc-quote__body' }, p.body) : null,
      (p.lede || p.body) && p.quote ? h('hr', { className: 'dc-quote__rule' }) : null,
      p.quote ? h('blockquote', { className: 'dc-quote__quote' }, p.quote,
        p.cite ? h('cite', { className: 'dc-quote__cite' }, '– ' + p.cite) : null) : null);
  }

  window.DAOcubator = { Panel: Panel, HungPanel: HungPanel, NodeCard: NodeCard, ComparisonTable: ComparisonTable, PullQuote: PullQuote };
})();
