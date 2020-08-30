#include <SFML/Graphics.hpp>
#include <QTextStream>

int main()
{
	sf::RenderWindow window(sf::VideoMode(500,500), "Let's Play Hangman");
    sf::RectangleShape startButton(sf::Vector2f(80,50));
    startButton.setFillColor(sf::Color::Green);
    startButton.setPosition(200.f, 200.f);

	while (window.isOpen())
	{
		sf::Event event;
		while (window.pollEvent(event))
		{


            if(event.type == sf::Event::Closed)
			window.close();
		}
		window.clear();
        window.draw(startButton);
		window.display();
	}
	return 0;
}
