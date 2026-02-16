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
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#1a1a2e',
        fontSize: 80,
        fontWeight: 'bold',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '30px',
          maxWidth: '1800px',
        }}
      >
        {words.map((word, index) => {
          // Each word appears at a different time
          const startFrame = index * 25; // Start every 25 frames

          // Opacity animation (fade in)
          const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], {
            extrapolateRight: 'clamp',
          });

          // Scale animation (spring effect)
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
                color: colors[index % colors.length],
                opacity,
                transform: `scale(${scale})`,
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
          fontSize: 40,
          color: '#ffffff',
          opacity: interpolate(frame, [200, 240], [0, 1], {
            extrapolateRight: 'clamp',
          }),
        }}
      >
        Video Renderizado en Easypanel 🚀
      </div>
    </AbsoluteFill>
  );
};
