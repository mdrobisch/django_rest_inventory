import FontAwesome from '@expo/vector-icons/FontAwesome';
// ...existing code...
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { useFonts } from 'expo-font';
// Removed unused Drawer import
import * as SplashScreen from 'expo-splash-screen';
import { useEffect } from 'react';
import 'react-native-reanimated';
import { DrawerContentScrollView, DrawerItemList } from '@react-navigation/drawer';
import {
	Platform,
} from 'react-native';
import { Drawer } from 'expo-router/drawer';
import { useColorScheme } from '@/components/useColorScheme';
import { AppProviders, AuthGate } from '../context/Providers';

export {
  // Catch any errors thrown by the Layout component.
  ErrorBoundary,
} from 'expo-router';

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [loaded, error] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
    ...FontAwesome.font,
  });

  useEffect(() => {
    if (error) throw error;
  }, [error]);

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  if (!loaded) {
    return null;
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <AppProviders>
						<Drawer
							screenOptions={{
								drawerItemStyle: { display: 'none' },
								headerShown: true,
								// Adding specific configuration for gesture handling
								//swipeEnabled: Platform.OS !== 'web',
							}}
							initialRouteName="items"
						>
          <Drawer.Screen
            name="index"
            options={{
              drawerLabel: 'Items',
              title: 'Items',
            }}
          />
          <Drawer.Screen
            name="items"
            options={{
              drawerLabel: 'Items',
              drawerItemStyle: { display: 'flex' },
              title: 'Items',
            }}
          />
          <Drawer.Screen
            name="login"
            options={{
              drawerLabel: 'Login',
              drawerItemStyle: { display: 'flex' },
              title: 'Login',
            }}
          />

        </Drawer>
      </AppProviders>
    </GestureHandlerRootView>
  );
}

// If you need to access the token in _layout.tsx for web, use:
// const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
