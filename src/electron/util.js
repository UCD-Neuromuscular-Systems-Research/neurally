export function isDev() {
  // eslint-disable-next-line no-undef
  return process.env.NODE_ENV === 'development'; // process is defined in node js environment where the app runs
}
