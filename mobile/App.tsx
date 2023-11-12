import React from 'react';
import { StyleSheet, View } from 'react-native';
import WebView from 'react-native-webview';

const App = () => (
  <View style={styles.container}>
    <WebView source={{ uri: 'http://pama.vip/gpt' }} />
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default App;