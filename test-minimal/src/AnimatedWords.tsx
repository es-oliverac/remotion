import {AbsoluteFill, useCurrentFrame, interpolate, spring} from 'remotion';

interface AnimatedWordsProps {
  words?: string[];
  title?: string;
  subtitle?: string;
  backgroundColor?: string;
}

const colors = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
  '#DFE6E9', '#FD79A8', '#A29BFE', '#F39C12', '#E74C3C',
  '#9B59B6', '#3498DB', '#1ABC9C', '#2ECC71', '#E67E22'
];

export const AnimatedWords: React.FC<AnimatedWordsProps> = ({
  words = ['PALABRA', '1', 'PALABRA', '2', 'PALABRA', '3'],
  title = '',
  subtitle = '',
  backgroundColor = '#1a1a2e'
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
      }}
    >
      {/* Title (optional) */}
      {title && (
        <div
          style={{
            position: 'absolute',
            top: '15%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            fontSize: 90,
            fontWeight: 900,
            color: '#ffffff',
            fontFamily: 'Arial, Helvetica, sans-serif',
            textAlign: 'center',
            opacity: interpolate(frame, [0, 30], [0, 1], {
              extrapolateRight: 'clamp',
            }),
            textShadow: '4px 4px 8px rgba(0,0,0,0.8)',
          }}
        >
          {title}
        </div>
      )}

      {/* Animated words */}
      <div
        style={{
          position: 'absolute',
          top: title ? '50%' : '45%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '35px',
          maxWidth: '1700px',
        }}
      >
        {words.map((word, index) => {
          const startFrame = title ? 45 + index * 25 : 15 + index * 25;
          const color = colors[index % colors.length];

          // Fade in
          const opacity = interpolate(frame, [startFrame, startFrame + 15], [0, 1], {
            extrapolateRight: 'clamp',
          });

          // Scale spring
          const scale = spring({
            frame: frame - startFrame,
            fps: 30,
            config: {
              damping: 10,
              stiffness: 100,
            },
          });

          // Slide from bottom
          const translateY = interpolate(
            frame,
            [startFrame, startFrame + 20],
            [80, 0],
            { extrapolateRight: 'clamp' }
          );

          return (
            <div
              key={index}
              style={{
                fontSize: 70,
                fontWeight: 900,
                color,
                opacity,
                transform: `scale(${scale}) translateY(${translateY}px)`,
                fontFamily: 'Arial, Helvetica, sans-serif',
                textShadow: `3px 3px 6px rgba(0,0,0,0.7)`,
              }}
            >
              {word}
            </div>
          );
        })}
      </div>

      {/* Subtitle (optional) */}
      {subtitle && (
        <div
          style={{
            position: 'absolute',
            bottom: 80,
            left: '50%',
            transform: 'translateX(-50%)',
            fontSize: 35,
            color: '#ffffff',
            fontWeight: 700,
            fontFamily: 'Arial, Helvetica, sans-serif',
            textAlign: 'center',
            opacity: interpolate(frame, [200, 240], [0, 1], {
              extrapolateRight: 'clamp',
            }),
            textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
          }}
        >
          {subtitle}
        </div>
      )}
    </AbsoluteFill>
  );
};
