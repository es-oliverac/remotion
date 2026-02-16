import {AbsoluteFill, useCurrentFrame, interpolate, spring} from 'remotion';

export const HelloWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [0, 30],
    [0, 1],
    {
      extrapolateRight: 'clamp',
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
        backgroundColor: '#000000',
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: `translate(-50%, -50%) scale(${scale})`,
          fontSize: 120,
          fontWeight: 900,
          color: '#ffffff',
          textAlign: 'center',
          fontFamily: 'Arial, Helvetica, sans-serif',
          opacity,
          textShadow: '4px 4px 8px rgba(0,0,0,0.8)',
          WebkitTextStroke: '1px rgba(255,255,255,0.3)',
        }}
      >
        HOLA DESDE REMOTION!
      </div>
    </AbsoluteFill>
  );
};
