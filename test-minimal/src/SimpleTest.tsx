import {AbsoluteFill} from 'remotion';

export const SimpleTest: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: 'red',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          fontSize: 100,
          fontWeight: 'bold',
          color: 'white',
          textAlign: 'center',
        }}
      >
        SI VEO ESTO, FUNCIONA
      </div>
    </AbsoluteFill>
  );
};
