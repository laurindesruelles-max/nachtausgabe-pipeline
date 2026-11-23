import React from "react";
import {Composition, AbsoluteFill, useCurrentFrame} from "remotion";
import {FPS, Drift} from "./lib";
import * as C from "./comps";

const MAP: Record<string, React.FC<any>> = {map: C.MapC, flow: C.FlowC, flip: C.FlipC, counter: C.CounterC, grid: C.GridC, phone: C.PhoneC, cipher: C.CipherC, stack: C.StackC, bars: C.BarsC};
const Grain: React.FC = () => {
  const f = useCurrentFrame(); const seed = Math.floor(f / 2) % 7;
  return <AbsoluteFill style={{pointerEvents: "none", mixBlendMode: "overlay", opacity: 0.18}}><svg width="100%" height="100%"><filter id={`g${seed}`}><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed={seed} /></filter><rect width="100%" height="100%" filter={`url(#g${seed})`} /></svg></AbsoluteFill>;
};
const Motion: React.FC<any> = ({comp, props, len}) => {
  const Comp = MAP[comp];
  return <AbsoluteFill style={{background: "#000"}}><Drift len={len}><Comp {...props} len={len} /></Drift><Grain /></AbsoluteFill>;
};
export const Root: React.FC = () => (
  <Composition id="Motion" component={Motion} fps={FPS} width={1920} height={1080} durationInFrames={180}
    defaultProps={{comp: "counter", props: {value: 1000, caption: "TEST"}, len: 6}}
    calculateMetadata={({props}: any) => ({durationInFrames: Math.round((props.len || 6) * FPS)})} />
);
