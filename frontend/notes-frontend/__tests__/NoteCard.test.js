import { render, screen } from '@testing-library/react';
import NoteCard from '../components/NoteCard';

describe('NoteCard Component', () => {
  const note = {
    title: 'Test Note',
    content: 'This is a test note content',
  };

  it('renders the note title and content', () => {
    render(<NoteCard note={note} />);
    expect(screen.getByText('Test Note')).toBeInTheDocument();
    expect(screen.getByText('This is a test note content')).toBeInTheDocument();
  });
});
