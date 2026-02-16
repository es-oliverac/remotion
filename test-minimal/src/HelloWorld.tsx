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
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: 100,
        fontWeight: 'bold',
        color: '#ffffff',
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          textAlign: 'center',
        }}
      >
        HOLA DESDE REMOTION!
      </div>
    </AbsoluteFill>
  );
};
