// NACHTAUSGABE-Look: Comicseite (Graphic Novel Noir). Schwarz, Papierweiß, Bernstein. Grafiken stehen in einem Comic-Panel
// mit dickem Tuscherahmen auf der Seite (Kamera bleibt auf der Seite), Rasterpunkte, Bangers + Comic Neue, Erzählkästchen,
// Sprechblasen, Tusche-Silhouetten als Symbole, Zeitungsausschnitt statt Akte, Fahndungsplakat statt Karteikarte.
import React from "react";
import {AbsoluteFill, useCurrentFrame, interpolate} from "remotion";
import {s, clamp, ease} from "./lib";

const INK = "#0E0C0A", PAPER = "#ECE2CC", AMBER = "#F0B01E", DIM = "#6b6152";
const HEAD = "Bangers, cursive", BODY = "'Comic Neue', sans-serif";
const halftone = (c: string, size = 9, op = 0.22) => `radial-gradient(${c} ${size * 0.22}px, transparent ${size * 0.24}px) 0 0 / ${size}px ${size}px`;

const Bg: React.FC<{children?: React.ReactNode; hot?: boolean}> = ({children, hot}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: "#050404"}}>
      {/* Nachbar-Panels am Rand: die Kamera bleibt auf der Comicseite */}
      <div style={{position: "absolute", left: -260, top: 40, width: 290, height: 1000, background: PAPER, border: `8px solid ${INK}`, opacity: 0.55}} />
      <div style={{position: "absolute", right: -260, top: 40, width: 290, height: 470, background: PAPER, border: `8px solid ${INK}`, opacity: 0.55}} />
      <div style={{position: "absolute", right: -260, top: 530, width: 290, height: 510, background: "#d8cdb5", border: `8px solid ${INK}`, opacity: 0.55}} />
      <div style={{position: "absolute", left: 46, top: 30, right: 46, bottom: 30, background: hot ? "#2a1a05" : PAPER, border: `10px solid ${INK}`, overflow: "hidden"}}>
        <div style={{position: "absolute", inset: 0, background: halftone(hot ? "rgba(240,176,30,0.35)" : "rgba(14,12,10,0.16)"), maskImage: "radial-gradient(ellipse at 70% 30%, transparent 25%, black 85%)"}} />
        {hot && <div style={{position: "absolute", inset: 0, background: `repeating-conic-gradient(from ${f * 0.4}deg at 50% 50%, rgba(240,176,30,0.22) 0deg 4deg, transparent 4deg 14deg)`}} />}
        <div style={{position: "absolute", inset: 0, transform: "translate(-46px,-30px)"}}>{children}</div>
      </div>
    </AbsoluteFill>
  );
};

/** Erzähltext erscheint Wort für Wort (Comic Neue) */
const Write: React.FC<{text: string; at: number; style?: React.CSSProperties}> = ({text, at, style}) => {
  const f = useCurrentFrame(); if (f < s(at)) return null;
  const words = text.split(" "); const n = ((f - s(at)) / 30) * 6;
  return <span style={{fontFamily: BODY, fontWeight: 700, ...style}}>{words.map((w, i) => <span key={i} style={{opacity: n > i ? 1 : 0}}>{w}{i < words.length - 1 ? " " : ""}</span>)}</span>;
};
/** Erzählkästchen (Bernstein, Tuscherahmen) oben links */
const Label: React.FC<{text?: string}> = ({text}) => {
  const f = useCurrentFrame(); if (!text) return null;
  const p = interpolate(f, [s(0.05), s(0.3)], [0, 1], {...clamp, easing: ease});
  return <div style={{position: "absolute", left: 90, top: 60, background: AMBER, border: `5px solid ${INK}`, padding: "6px 22px", transform: `scale(${0.8 + 0.2 * p})`, opacity: p, transformOrigin: "left top", boxShadow: `8px 8px 0 ${INK}`}}>
    <span style={{fontFamily: BODY, fontWeight: 700, fontSize: 32, color: INK, textTransform: "uppercase"}}>{text}</span></div>;
};
/** Bernstein-Route wie auf dem Comic-Stadtplan (gestrichelt, mit Tusche-Kontur) */
const Thread: React.FC<{x1: number; y1: number; x2: number; y2: number; p: number; straight?: boolean}> = ({x1, y1, x2, y2, p, straight}) => {
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - (straight ? 0 : Math.hypot(x2 - x1, y2 - y1) * 0.12);
  const len = Math.hypot(x2 - x1, y2 - y1) * 1.2; const d = `M${x1},${y1} Q${mx},${my} ${x2},${y2}`;
  return <g style={{clipPath: undefined}}><path d={d} fill="none" stroke={INK} strokeWidth={11} strokeDasharray={len} strokeDashoffset={len * (1 - p)} strokeLinecap="round" />
    <path d={d} fill="none" stroke={AMBER} strokeWidth={5} strokeDasharray={len} strokeDashoffset={len * (1 - p)} strokeLinecap="round" /></g>;
};
/** Tatort-Kreuz im Comic-Burst */
const Pin: React.FC<{x: number; y: number; k: number}> = ({x, y, k}) => (
  <g transform={`translate(${x},${y}) scale(${k})`}>
    <path d="M0 -26 L7 -9 L25 -12 L12 2 L22 18 L4 11 L-6 26 L-8 8 L-26 6 L-12 -6 L-20 -22 L-4 -12 Z" fill={AMBER} stroke={INK} strokeWidth={4} />
    <path d="M-7 -7 L7 7 M7 -7 L-7 7" stroke={INK} strokeWidth={5} strokeLinecap="round" />
  </g>
);
/* ---- Nachtausgabe-eigene Symbole: Tusche-Silhouetten (gefüllt schwarz, weiße Glanzkante) ---- */
const S = (c: string) => ({fill: c, stroke: "none"});
const icons: Record<string, (st: any, c: string) => React.ReactNode> = {
  person: (st, c) => <g {...S(c)}><path d="M28 30 h44 l-6 -14 h-32 z M24 32 h52 v5 h-52z" /><circle cx={50} cy={46} r={12} /><path d="M24 96 C24 70 34 60 50 60 C66 60 76 70 76 96 Z" /><path d="M38 60 L50 78 L62 60" fill="#ECE2CC" /></g>,
  gun: (st, c) => <path {...S(c)} d="M8 36 H80 V50 H58 L54 58 H44 L40 70 L28 90 H14 L24 58 L8 52 Z M82 38 H92 V46 H82 Z" />,
  car: (st, c) => <g {...S(c)}><path d="M4 66 V52 L18 50 L30 32 H66 L80 50 L96 54 V66 Z" /><circle cx={26} cy={70} r={11} /><circle cx={76} cy={70} r={11} /><path d="M36 38 H48 V50 H30Z M54 38 H64 L72 50 H54Z" fill="#ECE2CC" /></g>,
  money: (st, c) => <g><path {...S(c)} d="M10 26 H90 V74 H10 Z" /><text x={50} y={60} textAnchor="middle" fontFamily={HEAD} fontSize={36} fill="#ECE2CC">$</text></g>,
  doc: (st, c) => <g><path {...S(c)} d="M18 6 H82 V94 H18 Z" /><path d="M26 16 H74 V30 H26Z" fill="#ECE2CC" /><path d="M26 40 H74 M26 50 H74 M26 60 H60 M26 70 H70" stroke="#ECE2CC" strokeWidth={4} /></g>,
  lock: (st, c) => <g><path d="M32 46 V30 a18 18 0 0 1 36 0 V46" stroke={c} strokeWidth={10} fill="none" /><rect {...S(c)} x={20} y={44} width={60} height={50} rx={4} /><circle cx={50} cy={66} r={6} fill="#ECE2CC" /></g>,
  phone: (st, c) => <g><path {...S(c)} d="M14 40 C14 20 86 20 86 40 L76 46 L68 36 H32 L24 46 Z" /><path {...S(c)} d="M30 50 H70 L80 90 H20 Z" /><circle cx={50} cy={68} r={10} fill="#ECE2CC" /></g>,
  eye: (st, c) => <g><path {...S(c)} d="M4 50 C24 16 76 16 96 50 C76 84 24 84 4 50 Z" /><circle cx={50} cy={50} r={16} fill="#ECE2CC" /><circle cx={50} cy={50} r={8} fill={c} /></g>,
  clock: (st, c) => <g><circle {...S(c)} cx={50} cy={50} r={44} /><circle cx={50} cy={50} r={34} fill="#ECE2CC" /><path d="M50 24 V50 L66 60" stroke={c} strokeWidth={7} fill="none" /></g>,
  gavel: (st, c) => <g {...S(c)}><path d="M20 36 L48 8 L62 22 L34 50 Z" /><path d="M44 36 L52 28 L88 64 L80 72 Z" /><rect x={10} y={84} width={50} height={10} /></g>,
  ship: (st, c) => <path {...S(c)} d="M4 60 H96 L82 88 H18 Z M26 58 V38 H66 V58 Z M42 36 V16 H52 V36 Z" />,
  bank: (st, c) => <path {...S(c)} d="M50 4 L94 28 V36 H6 V28 Z M14 42 H26 V80 H14Z M34 42 H46 V80 H34Z M54 42 H66 V80 H54Z M74 42 H86 V80 H74Z M6 84 H94 V94 H6Z" />,
  knife: (st, c) => <path {...S(c)} d="M10 90 L20 80 L26 86 L16 96 Z M24 78 L86 8 C94 30 80 52 34 88 Z" />,
  badge: (st, c) => <g><path {...S(c)} d="M50 4 L60 30 L88 30 L66 48 L74 76 L50 60 L26 76 L34 48 L12 30 L40 30 Z" /><circle cx={50} cy={42} r={10} fill="#ECE2CC" /></g>,
  factory: (st, c) => <path {...S(c)} d="M6 92 V46 L30 60 V46 L54 60 V20 H70 V92 Z" />,
};
/** Station = kleines Comic-Panel mit Tuscherahmen und Speedlines */
const Node: React.FC<{hot?: boolean; children?: React.ReactNode}> = ({hot, children}) => (
  <div style={{width: 200, height: 180, margin: "0 auto", position: "relative", background: hot ? AMBER : PAPER, border: `7px solid ${INK}`, boxShadow: `10px 10px 0 ${INK}`, transform: "rotate(-1.5deg)", overflow: "hidden",
    display: "flex", alignItems: "center", justifyContent: "center"}}>
    <div style={{position: "absolute", inset: 0, background: `repeating-conic-gradient(from 0deg at 50% 55%, rgba(14,12,10,${hot ? 0.25 : 0.12}) 0deg 3deg, transparent 3deg 12deg)`}} />
    <div style={{position: "relative"}}>{children}</div>
  </div>
);
/** Raster: Fahndungs-Mini-Plakate (GESUCHT), betroffene mit Bernstein-Balken */
const Tile: React.FC<{hot?: boolean; icon?: string}> = ({hot, icon}) => (
  <div style={{width: 62, height: 72, background: hot ? AMBER : PAPER, border: `4px solid ${INK}`, display: "flex", flexDirection: "column", alignItems: "center", boxShadow: `4px 4px 0 ${INK}`}}>
    <div style={{fontFamily: HEAD, fontSize: 12, color: INK, lineHeight: 1.2, letterSpacing: 1}}>GESUCHT</div>
    <svg width={44} height={46} viewBox="0 0 100 100">{(icons[icon || "person"] || icons.person)({}, INK)}</svg>
  </div>
);

export const T = {
  c: {ink: INK, muted: DIM, accent: INK, hot: "#C8102E", land: "#d9cdb3", border: INK, dot: INK, hl: (o: number) => `rgba(240,176,30,${0.35 + 0.5 * o})`,
      track: "#b9ac90", panelAccent: INK, nodeInk: INK, panelInk: INK, cardInk: INK, cardHotInk: INK, tileInk: INK, bubble: "#7a5a10", sheetInk: INK, sheetLine: "#b9ac90"},
  font: {head: HEAD, body: BODY, num: HEAD, mono: "DejaVu Sans Mono, monospace"},
  headWeight: 400, headStyle: {letterSpacing: 2, WebkitTextStroke: `2px ${INK}`, color: AMBER, textShadow: `6px 6px 0 ${INK}`} as React.CSSProperties, iconStroke: 6,
  iconFilter: undefined as string | undefined, mapFilter: undefined as string | undefined,
  glow: false, borderW: 2.2, tileJitter: 5, gridRows: false, num: {sep: ".", decSep: ","},
  Bg, Write, Label, Thread, Pin, icons, Node, Tile, symbolStyle: {color: AMBER, WebkitTextStroke: `7px ${INK}`, textShadow: `12px 12px 0 ${INK}`, transform: "rotate(8deg)"} as React.CSSProperties, counterPad: "20px 60px 30px",
  tag: {background: "#FFFFFF", border: `4px solid ${INK}`, borderRadius: 24, padding: "2px 18px", boxShadow: `5px 5px 0 ${INK}`} as React.CSSProperties, tagText: {color: INK, fontSize: 30} as React.CSSProperties,
  panel: {background: "#f6efdd", border: `8px solid ${INK}`, boxShadow: `14px 14px 0 ${INK}`, padding: "10px 40px", transform: "rotate(-1deg)"} as React.CSSProperties,
  node: {} as React.CSSProperties, nodeHot: {} as React.CSSProperties,
  card: {background: "#f6efdd", border: `10px solid ${INK}`, boxShadow: `16px 16px 0 ${INK}`} as React.CSSProperties,
  cardTop: "GESUCHT", cardTopStyle: {fontFamily: HEAD, fontSize: 64, color: INK, letterSpacing: 4, left: 0, right: 0, textAlign: "center"} as React.CSSProperties,
  cardHot: {background: AMBER, border: `10px solid ${INK}`, boxShadow: `16px 16px 0 ${INK}`} as React.CSSProperties,
  tile: {} as React.CSSProperties, tileHot: {} as React.CSSProperties,
  sheet: {background: "#f6efdd", border: `6px solid ${INK}`, boxShadow: `10px 10px 0 ${INK}`} as React.CSSProperties,
  bar: {background: `${INK}`, border: `4px solid ${INK}`} as React.CSSProperties,
  barHot: {background: AMBER, border: `5px solid ${INK}`, boxShadow: `6px 6px 0 ${INK}`} as React.CSSProperties,
  phoneFrame: {background: INK, border: `6px solid ${INK}`} as React.CSSProperties,
};
