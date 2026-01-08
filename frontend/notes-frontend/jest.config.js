module.exports = {
    testEnvironment: "jest-environment-jsdom",                   // simulate browser environment
    setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],  // run setup before tests
    moduleNameMapper: {
      "\\.(css|scss)$": "identity-obj-proxy",   // mock CSS imports
    },
  };
  