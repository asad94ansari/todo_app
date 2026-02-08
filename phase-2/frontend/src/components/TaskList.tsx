import React from 'react';
import { Todo } from '@/types/todo';
import { CheckCircle, Circle, Trash2 } from 'lucide-react';

interface TaskListProps {
  todos: Todo[];
  onToggle: (id: number, completed: boolean) => void;
  onDelete: (id: number) => void;
}

export default function TaskList({ todos, onToggle, onDelete }: TaskListProps) {
  if (todos.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No todos yet. Add one to get started!</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      <ul className="divide-y divide-gray-200">
        {todos.map((todo) => (
          <li key={todo.id}>
            <div className="px-4 py-4 sm:px-6 flex items-center justify-between">
              <div className="flex items-center">
                <button
                  onClick={() => onToggle(todo.id, todo.completed)}
                  className="mr-3 focus:outline-none"
                >
                  {todo.completed ? (
                    <CheckCircle className="h-6 w-6 text-green-500" />
                  ) : (
                    <Circle className="h-6 w-6 text-gray-400" />
                  )}
                </button>
                <div>
                  <p
                    className={`text-sm font-medium ${
                      todo.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                    }`}
                  >
                    {todo.title}
                  </p>
                  {todo.description && (
                    <p className="mt-1 text-sm text-gray-500">{todo.description}</p>
                  )}
                </div>
              </div>
              <div className="flex items-center">
                <span className="text-xs text-gray-500 mr-4">
                  {new Date(todo.created_at).toLocaleDateString()}
                </span>
                <button
                  onClick={() => onDelete(todo.id)}
                  className="text-red-600 hover:text-red-900 focus:outline-none"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}