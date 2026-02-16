import {AbsoluteFill, Sequence, useCurrentFrame, interpolate, spring} from 'remotion';

export const HelloWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [30, 90],
    [0, 1],
    {
      extrapolateRight: false,
    }
  );

  const scale = spring({
    frame,
    fps: 30,
    config: {
      damping: 10,
    },
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: 80,
        fontWeight: 'bold',
        background: '#000',
        color: '#fff',
      }}
    >
      <div style={{opacity, transform: `scale(${scale})`}}>
        HOLA DESDE REMOTION!
      </div>
    </AbsoluteFill>
  );
};
