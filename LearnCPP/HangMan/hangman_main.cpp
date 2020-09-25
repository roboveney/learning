#include <SFML/System/String.hpp>
#include <SFML/Graphics/Export.hpp>
#include <SFML/Graphics/Glyph.hpp>
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/OpenGL.hpp>
#include <QTextStream>
#include <iostream>
using namespace std;

/*Primary goal with this program is to attempt to code a game of hangman from scratch without looking at a specific tutorial but instead
 * working from psuedo code to attempt to create the game and referencing small tutorials and lessons as I go to accomplish to overall game*/

/*CURRENT STATUS: need to figure out how to get text to display in the new cleared version of the window after start button is pressed and
and create a game over sprite or text*/

//Function to see if mouse is over a button
bool isHover(sf::FloatRect button, sf::Vector2f mouse)
{
    if (button.contains(mouse))
    {
        return true;
    }
    return false;
}

int main()
{
    //initialize variables used throughout gameplay
    int win_height = 600;
    int win_width = 1000;
    bool isPlaying = false;
    bool gameLost = false;
    sf::Font font;

    //Load and check the availability of the font file
    if(!font.loadFromFile("fonts/arial.ttf"))
    {
        cout << "can't load font" << endl;
    }

    //create game window with label
    sf::RenderWindow window(sf::VideoMode(win_width,win_height), "Let's Play Hangman");
    sf::Vector2i mousePos = sf::Mouse::getPosition(window);

    //generate start button
    sf::CircleShape startButton;
    startButton.setRadius(50);
    startButton.setPosition((win_width/2)-25, (win_height/2)-25);
    float startButtonWidth = startButton.getLocalBounds().width;
    float startButtonHeight = startButton.getLocalBounds().height;
    sf::Texture texture;
    if (!texture.loadFromFile(("start-button.png")))
        return -1;
    startButton.setTexture(&texture);


    while (window.isOpen())
    {
        //passively look for events
        sf::Event event;
        while (window.pollEvent(event))
        {
            //handle closing of window
            if(event.type == sf::Event::Closed)
                window.close();

            //was the start button clicked
            if(isHover(startButton.getGlobalBounds(), sf::Vector2f(event.mouseButton.x, event.mouseButton.y)) == true)
            {
                if(event.type == sf::Event::MouseButtonReleased &&  event.mouseButton.button == sf::Mouse::Left)
                {
                    cout <<"confirmation"<<endl;
                    isPlaying = true;
                }
            }
            if(isPlaying)
            {
                window.clear(sf::Color::Blue);
                window.display();

                sf::Text text;
                text.setString("Hello world");
                text.setCharacterSize(30);
                text.setFillColor(sf::Color::Red);
                text.setStyle(sf::Text::Bold | sf::Text::Underlined);
                window.draw(text);
            }
            if(!isPlaying)
            {
                window.clear();
                if(!gameLost)
                {
                    window.draw(startButton);
                }else{
                    //window.draw(gameOver);
                }
                window.display();
            }
        }
    }
    return 0;
}
