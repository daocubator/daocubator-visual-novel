import type { ReactNode } from 'react';

/** A raised content panel (`char`) with an optional glow sans title. Stack several for the layered look. */
export interface PanelProps {
  /** Glow `panel-title` line, e.g. "Layer 2: The Root System (DAOs)". */
  title?: ReactNode;
  /** Body copy in `bone`. */
  children?: ReactNode;
  /** `default` = char fill; `deep` = ground fill for alternating stacks. */
  tone?: 'default' | 'deep';
  /** Adds a `rule-strong` hairline frame. */
  framed?: boolean;
  className?: string;
}
export declare function Panel(props: PanelProps): JSX.Element;

/** A panel hung on visible twine inside an oversized timber frame, wall showing on every side. For dialogue boxes, portraits, inventory slots and menu panels. */
export interface HungPanelProps {
  /** Glow `panel-title` line. */
  title?: ReactNode;
  /** Body copy in `bone`. Keep to two or three lines. */
  children?: ReactNode;
  className?: string;
}
export declare function HungPanel(props: HungPanelProps): JSX.Element;

/** A glowing ring holding a line icon, beside a labelled card. */
export interface NodeCardProps {
  /** Uppercase category, e.g. "CULTURE". */
  label?: ReactNode;
  /** `Name: what it does` description. */
  children?: ReactNode;
  /** A line SVG (stroke inherits glow). */
  icon?: ReactNode;
  /** Ring on the left (default) or right of the card. */
  side?: 'left' | 'right';
  className?: string;
}
export declare function NodeCard(props: NodeCardProps): JSX.Element;

/** A sand-hairline grid comparing models across rows. */
export interface ComparisonTableProps {
  /** Column headings, e.g. ["The For-Profit Model", "The For-Product Model"]. */
  columns: ReactNode[];
  /** One entry per row: a field label cell plus one cell per column. */
  rows: { label: ReactNode; cells: ReactNode[] }[];
  /** Optional top-left cell content. */
  corner?: ReactNode;
  className?: string;
}
export declare function ComparisonTable(props: ComparisonTableProps): JSX.Element;

/** The statement pattern: flame lede with a bold glow close, body, rule, serif quote and attribution. Any part optional. */
export interface PullQuoteProps {
  lede?: ReactNode;
  /** Bold glow closing phrase on its own line. */
  emphasis?: ReactNode;
  body?: ReactNode;
  quote?: ReactNode;
  /** Name only; the en dash is added. */
  cite?: string;
  className?: string;
}
export declare function PullQuote(props: PullQuoteProps): JSX.Element;
