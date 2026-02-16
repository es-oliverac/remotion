import {AbsoluteFill, useCurrentFrame, interpolate, spring, Series} from 'remotion';

interface CustomTextProps {
  title?: string;
  subtitle?: string;
  words?: string[];
}

const defaultWords = [
  'VIDEO',
  'PERSONALIZADO',
  'DESDE',
  'N8N',
  '💪'
];

export const CustomText: React.FC<CustomTextProps> = ({
  title = 'TEXTO ANIMADO',
  subtitle = 'Renderizado con Remotion + FastAPI',
  words = defaultWords,
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        background: 'linear-gradient(to bottom, #667eea 0%, #764ba2 100%)',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      {/* Title */}
      <div
        style={{
          fontSize: 120,
          fontWeight: 'bold',
          color: '#fff',
          textAlign: 'center',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateRight: 'clamp',
          }),
          transform: `scale(${spring({
            frame,
            fps: 30,
            config: { damping: 10 },
          })})`,
          textShadow: '0 4px 20px rgba(0,0,0,0.3)',
          marginBottom: 100,
        }}
      >
        {title}
      </div>

      {/* Animated Words */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '40px',
          maxWidth: '1600px',
        }}
      >
        {words.map((word, index) => {
          const startFrame = 60 + index * 30;
          const color = `hsl(${(index * 60) % 360}, 70%, 60%)`;

          const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], {
            extrapolateRight: 'clamp',
          });

          const scale = spring({
            frame: frame - startFrame,
            fps: 30,
            config: { damping: 8, stiffness: 80 },
          });

          const translateY = interpolate(
            frame,
            [startFrame, startFrame + 25],
            [150, 0],
            { extrapolateRight: 'clamp' }
          );

          return (
            <div
              key={index}
              style={{
                fontSize: 70,
                fontWeight: 'bold',
                color,
                opacity: Math.max(0, Math.min(1, opacity)),
                transform: `scale(${scale}) translateY(${translateY}px)`,
                textShadow: `0 2px 10px ${color}`,
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
          bottom: 80,
          fontSize: 50,
          color: '#fff',
          fontWeight: 'bold',
          textAlign: 'center',
          opacity: interpolate(frame, [180, 220], [0, 1], {
            extrapolateRight: 'clamp',
          }),
          textShadow: '0 2px 10px rgba(0,0,0,0.3)',
        }}
      >
        {subtitle}
      </div>
    </AbsoluteFill>
  );
};
