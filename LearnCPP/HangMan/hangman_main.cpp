#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/OpenGL.hpp>
#include <QTextStream>
#include <iostream>
using namespace std;

/*Primary goal with this program is to attempt to code a game of hangman from scratch without looking at a specific tutorial but instead
 * working from psuedo code to attempt to create the game and referencing small tutorials and lessons as I go to accomplish to overall game*/

/*CURRENT STATUS: need to create function call for game now that start button works and apply texture to actual start button*/

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

    //create game window with label
    sf::RenderWindow window(sf::VideoMode(win_width,win_height), "Let's Play Hangman");
    sf::Vector2i mousePos = sf::Mouse::getPosition(window);

    //generate start button
    sf::RectangleShape startButton(sf::Vector2f(80,50));
    startButton.setFillColor(sf::Color::Green);
    startButton.setPosition(win_width/2, win_height/2);
    float startButtonWidth = startButton.getLocalBounds().width;
    float startButtonHeight = startButton.getLocalBounds().height;

    sf::Texture texture;
    if (!texture.loadFromFile(("start-button.png")))
        return -1;
    // Assign it to a sprite
    sf::Sprite sprite;
    sprite.setTexture(texture);
    sprite.scale(sf::Vector2f(.15f, .15f));


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
                }
            }
        }

        window.clear();
        window.draw(startButton);
        window.draw(sprite);
        window.display();
    }



    return 0;
}
