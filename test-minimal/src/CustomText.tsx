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
        backgroundColor: '#667eea',
      }}
    >
      {/* Title */}
      <div
        style={{
          position: 'absolute',
          top: '30%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          fontSize: 100,
          fontWeight: 900,
          color: '#ffffff',
          fontFamily: 'Arial, Helvetica, sans-serif',
          textAlign: 'center',
          opacity: interpolate(frame, [0, 30], [0, 1], {
            extrapolateRight: 'clamp',
          }),
          textShadow: '4px 4px 8px rgba(0,0,0,0.5)',
        }}
      >
        {title}
      </div>

      {/* Animated Words */}
      <div
        style={{
          position: 'absolute',
          top: '55%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
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
                fontWeight: 900,
                color,
                opacity,
                transform: `scale(${scale})`,
                fontFamily: 'Arial, Helvetica, sans-serif',
                textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
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
          left: '50%',
          transform: 'translateX(-50%)',
          fontSize: 40,
          color: '#ffffff',
          fontWeight: 700,
          fontFamily: 'Arial, Helvetica, sans-serif',
          textAlign: 'center',
          opacity: interpolate(frame, [180, 220], [0, 1], {
            extrapolateRight: 'clamp',
          }),
          textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
        }}
      >
        {subtitle}
      </div>
    </AbsoluteFill>
  );
};
