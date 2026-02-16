import {AbsoluteFill} from 'remotion';

export const SimpleTest: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: 'blue',
      }}
    >
      {/* Fondo blanco con forma de texto - fallback visual */}
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          fontSize: 100,
          fontWeight: 900,
          backgroundColor: 'white',
          color: 'white',
          padding: '20px 40px',
          borderRadius: '10px',
          fontFamily: 'Arial, Helvetica, sans-serif, sans-serif',
          WebkitFontSmoothing: 'antialiased',
          MozOsxFontSmoothing: 'grayscale',
        }}
      >
        TEXTO DE PRUEBA
      </div>

      {/* Rectángulo decorativo para verificar que se renderiza */}
      <div
        style={{
          position: 'absolute',
          bottom: 100,
          left: '50%',
          transform: 'translateX(-50%)',
          width: 400,
          height: 50,
          backgroundColor: 'yellow',
          borderRadius: '5px',
        }}
      />
    </AbsoluteFill>
  );
};
