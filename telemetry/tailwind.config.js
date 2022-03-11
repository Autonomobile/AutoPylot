module.exports = {
  content: ["./pages/**/*.js", "./components/**/*.js"],
  theme: {
    extend: {
      flex: {
        '0': '0 1 0%'
      },
      boxShadow: {
        'google': '0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);',
      }
    },
  },
  plugins: [],
};
