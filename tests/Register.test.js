import { render, screen } from '@testing-library/react';
import Register from './Register';

test('renders register form', () => {
    render(<Register />);
    const linkElement = screen.getByText(/Register/i);
    expect(linkElement).toBeInTheDocument();
});
