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
  const totalFrames = 300; // 10 seconds at 30fps

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
        fontSize: 100,
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
          const duration = 40; // Animation duration

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

          // Rotation animation
          const rotation = interpolate(
            frame,
            [startFrame, startFrame + duration],
            [-15, 0],
            {
              extrapolateRight: 'clamp',
            }
          );

          // Slide from bottom
          const translateY = interpolate(
            frame,
            [startFrame, startFrame + 30],
            [100, 0],
            {
              extrapolateRight: 'clamp',
            }
          );

          return (
            <div
              key={index}
              style={{
                color: colors[index % colors.length],
                opacity: Math.max(0, Math.min(1, opacity)),
                transform: `scale(${scale}) rotate(${rotation}deg) translateY(${translateY}px)`,
                textShadow: `0 0 20px ${colors[index % colors.length]}80`,
                filter: `drop-shadow(0 4px 8px rgba(0,0,0,0.5))`,
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
          transform: `scale(${spring({
            frame: frame - 200,
            fps: 30,
            config: {
              damping: 10,
            },
          })})`,
        }}
      >
        Video Renderizado en Easypanel 🚀
      </div>
    </AbsoluteFill>
  );
};
