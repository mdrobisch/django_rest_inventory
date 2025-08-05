import React, { useState } from 'react';
import { View, Text, FlatList, ActivityIndicator, Button, TextInput, StyleSheet, Alert } from 'react-native';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api';

const fetchItems = async () => {
  const response = await api.get('/items/');
  return response.data;
};

const createItem = async (item: { name: string; description: string; quantity: number }) => {
  const response = await api.post('/items/', item);
  return response.data;
};

const deleteItem = async (id: number) => {
  await api.delete(`/items/${id}/`);
};

export default function ItemsScreen() {
  const queryClient = useQueryClient();
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['items'], 
    queryFn: fetchItems,
  });

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [quantity, setQuantity] = useState('');

  const mutation = useMutation({
    mutationFn: createItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
      setName('');
      setDescription('');
      setQuantity('');
    },
    onError: () => Alert.alert('Error', 'Could not create item'),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteItem,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['items'] }),
    onError: () => Alert.alert('Error', 'Could not delete item'),
  });

  if (isLoading) {
    return <ActivityIndicator size="large" />;
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Text>Error loading items.</Text>
        <Button title="Retry" onPress={() => refetch()} />
      </View>
    );
  }

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text style={styles.title}>Add Item</Text>
      <TextInput
        style={styles.input}
        placeholder="Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Description"
        value={description}
        onChangeText={setDescription}
      />
      <TextInput
        style={styles.input}
        placeholder="Quantity"
        value={quantity}
        onChangeText={setQuantity}
        keyboardType="numeric"
      />
      <Button
        title="Add Item"
        onPress={() => {
          const qty = parseInt(quantity, 10);
          if (isNaN(qty)) {
            Alert.alert('Error', 'Quantity must be a number');
            return;
          }
          mutation.mutate({ name, description, quantity: qty });
        }}
        disabled={!name || !quantity || mutation.status === 'pending'}
      />
      <Text style={styles.title}>Items</Text>
      <FlatList
        data={data}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.itemRow}>
            <View style={{ flex: 1 }}>
              <Text style={{ fontSize: 18 }}>{item.name}</Text>
              <Text style={{ color: '#888' }}>{item.description}</Text>
              <Text style={{ color: '#888' }}>Qty: {item.quantity}</Text>
            </View>
            <Button
              title="Delete"
              color="#d00"
              onPress={() => deleteMutation.mutate(item.id)}
            />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 22, fontWeight: 'bold', marginVertical: 12 },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 6, padding: 8, marginBottom: 8 },
  itemRow: { flexDirection: 'row', alignItems: 'center', padding: 12, borderBottomWidth: 1, borderColor: '#eee' },
});
