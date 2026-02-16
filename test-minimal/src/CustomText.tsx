import {AbsoluteFill, useCurrentFrame, interpolate, spring} from 'remotion';

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
        backgroundColor: '#667eea',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      {/* Title */}
      <div
        style={{
          fontSize: 100,
          fontWeight: 'bold',
          color: '#ffffff',
          textAlign: 'center',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateRight: 'clamp',
          }),
          transform: `scale(${spring({
            frame,
            fps: 30,
            config: { damping: 10 },
          })})`,
          marginBottom: 80,
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

          return (
            <div
              key={index}
              style={{
                fontSize: 60,
                fontWeight: 'bold',
                color,
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
          bottom: 80,
          fontSize: 40,
          color: '#ffffff',
          fontWeight: 'bold',
          textAlign: 'center',
          opacity: interpolate(frame, [180, 220], [0, 1], {
            extrapolateRight: 'clamp',
          }),
        }}
      >
        {subtitle}
      </div>
    </AbsoluteFill>
  );
};
