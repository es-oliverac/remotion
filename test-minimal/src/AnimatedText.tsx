import {AbsoluteFill, useCurrentFrame, interpolate, spring} from 'remotion';

// Palette of colors for words
const colors = [
  '#FF6B6B', // Red
  '#4ECDC4', // Teal
  '#45B7D1', // Blue
  '#96CEB4', // Green
  '#FFEAA7', // Yellow
  '#DFE6E9', // Gray
  '#FD79A8', // Pink
  '#A29BFE', // Purple
];

const words = [
  'HOLA',
  'DESDE',
  'EASYPANEL',
  'CON',
  'REMOTION',
  'Y',
  'FASTAPI',
  '🎬'
];

export const AnimatedText: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#1a1a2e',
      }}
    >
      {/* Main words container */}
      <div
        style={{
          position: 'absolute',
          top: '40%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '30px',
          maxWidth: '1800px',
        }}
      >
        {words.map((word, index) => {
          const startFrame = index * 25;

          const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], {
            extrapolateRight: 'clamp',
          });

          const scale = spring({
            frame: frame - startFrame,
            fps: 30,
            config: {
              damping: 12,
              stiffness: 100,
            },
          });

          return (
            <div
              key={index}
              style={{
                fontSize: 80,
                fontWeight: 900,
                color: colors[index % colors.length],
                opacity,
                transform: `scale(${scale})`,
                fontFamily: 'Arial, Helvetica, sans-serif',
                textShadow: `3px 3px 6px rgba(0,0,0,0.8)`,
              }}
            >
              {word}
            </div>
          );
        })}
      </div>

      {/* Subtitle */}
      <div
        style={{
          position: 'absolute',
          bottom: 100,
          left: '50%',
          transform: 'translateX(-50%)',
          fontSize: 40,
          fontWeight: 700,
          color: '#ffffff',
          fontFamily: 'Arial, Helvetica, sans-serif',
          opacity: interpolate(frame, [200, 240], [0, 1], {
            extrapolateRight: 'clamp',
          }),
          textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
        }}
      >
        Video Renderizado en Easypanel 🚀
      </div>
    </AbsoluteFill>
  );
};
