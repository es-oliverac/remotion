/**
 * Node.js wrapper for Remotion renderer
 * This script reads JSON from stdin and calls @remotion/renderer functions
 */

import { renderMedia, renderStill, getCompositions, selectComposition } from '@remotion/renderer';
import { readFileSync } from 'fs';

interface RenderMediaInput {
  serveUrl: string;
  composition: string;
  inputProps: Record<string, unknown>;
  outputPath: string;
  codec: 'h264' | 'h265' | 'vp8' | 'vp9' | 'prores';
  chromiumOptions?: {
    ignoreCertificateErrors?: boolean;
    disableWebSecurity?: boolean;
    gl?: string;
    headless?: boolean;
    userAgent?: string;
  };
  imageFormat: 'jpeg' | 'png' | 'webp';
  jpegQuality: number;
  scale: number;
  everyNthFrame: number;
  frameRange?: string;
  envVariables?: Record<string, string>;
  muted: boolean;
  overwrite: boolean;
  audioBitrate?: number;
  videoBitrate?: number;
  // Faster encoding options
  fps?: number;  // Reduce FPS for faster rendering
  enforceAudioTrack?: boolean;
  // FFmpeg optimization flags
  ffmpegCraneflag?: string[];
}

interface RenderStillInput {
  serveUrl: string;
  composition: string;
  inputProps: Record<string, unknown>;
  outputPath: string;
  frame: number;
  imageFormat: 'jpeg' | 'png' | 'webp' | 'pdf';
  jpegQuality: number;
  scale: number;
  overwrite: boolean;
}

interface GetCompositionsInput {
  serveUrl: string;
  inputProps?: Record<string, unknown>;
  envVariables?: Record<string, string>;
}

interface ProgressData {
  renderedFrames: number;
  encodedFrames: number;
  progress: number;
  stitchStage?: 'encoding' | 'muxing';
}

interface CliInput {
  command: 'renderMedia' | 'renderStill' | 'getCompositions';
  options: RenderMediaInput | RenderStillInput | GetCompositionsInput;
}

function writeOutput(data: { type: string; data?: unknown; message?: string }): void {
  process.stdout.write(JSON.stringify(data) + '\n');
}

function writeError(message: string): void {
  process.stderr.write(JSON.stringify({ type: 'error', message }) + '\n');
}

async function main() {
  try {
    // Read input from stdin
    const inputStr = readFileSync(0, 'utf-8').trim();
    const input: CliInput = JSON.parse(inputStr);

    writeOutput({ type: 'info', message: `Received command: ${input.command}` });

    if (input.command === 'renderMedia') {
      const opts = input.options as RenderMediaInput;

      writeOutput({ type: 'info', message: `Starting render for composition ${opts.composition}` });

      const composition = await selectComposition({
        serveUrl: opts.serveUrl,
        id: opts.composition,
        inputProps: opts.inputProps,
      });

      writeOutput({ type: 'info', message: `Selected composition: ${composition.id}` });

      await renderMedia({
        serveUrl: opts.serveUrl,
        composition,
        inputProps: opts.inputProps,
        outputLocation: opts.outputPath,
        codec: opts.codec,
        chromiumOptions: opts.chromiumOptions,
        imageFormat: opts.imageFormat,
        jpegQuality: opts.jpegQuality,
        scale: opts.scale,
        everyNthFrame: opts.everyNthFrame,
        envVariables: opts.envVariables,
        muted: opts.muted,
        overwrite: opts.overwrite,
        audioBitrate: opts.audioBitrate,
        videoBitrate: opts.videoBitrate,
        fps: opts.fps,
        enforceAudioTrack: opts.enforceAudioTrack,
        // Add FFmpeg optimization flags automatically
        ffmpegCraneflag: [
          // Use multiple threads for faster encoding
          '-threads',
          '8',
          // Faster encoding for H.264
          ...(opts.codec === 'h264' || opts.codec === 'h265' ? ['-preset', 'faster'] : []),
          // User-specified flags take precedence
          ...(opts.ffmpegCraneflag || [])
        ],
        onProgress: (progress: ProgressData) => {
          writeOutput({ type: 'progress', data: progress });
        },
      });

      writeOutput({ type: 'complete' });
    } else if (input.command === 'renderStill') {
      const opts = input.options as RenderStillInput;

      const composition = await selectComposition({
        serveUrl: opts.serveUrl,
        id: opts.composition,
        inputProps: opts.inputProps,
      });

      await renderStill({
        serveUrl: opts.serveUrl,
        composition,
        inputProps: opts.inputProps,
        output: opts.outputPath,
        frame: opts.frame,
        imageFormat: opts.imageFormat,
        jpegQuality: opts.jpegQuality,
        scale: opts.scale,
        overwrite: opts.overwrite,
      });

      writeOutput({ type: 'complete' });
    } else if (input.command === 'getCompositions') {
      const opts = input.options as GetCompositionsInput;

      const comps = await getCompositions(opts.serveUrl, {
        inputProps: opts.inputProps,
        envVariables: opts.envVariables,
      });

      writeOutput({
        type: 'compositions',
        data: comps.map((c) => ({
          id: c.id,
          width: c.width,
          height: c.height,
          fps: c.fps,
          durationInFrames: c.durationInFrames,
          defaultOutput: c.defaultProps,
        })),
      });
    } else {
      writeError(`Unknown command: ${input.command}`);
      process.exit(1);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    const stack = error instanceof Error ? error.stack : '';
    writeError(`${errorMessage}\nStack: ${stack}`);
    process.exit(1);
  }
}

main();
