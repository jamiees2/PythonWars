var game = new Phaser.Game(640, 480, Phaser.CANVAS, 'game');

var PythonWars = function (game) {

  this.map = null;
  this.layer = null;
  this.car = null;
  this.sprites = {};
};

var PythonSprite = function(id, x, y, sprite) {
  this.id = id;
  this.x = x;
  this.y = y;
  this.sprite = sprite;
};

PythonSprite.prototype = {
  init: function() {
    this.updatePos();
  },

  move: function(direction) {
    switch(direction) {
      case Phaser.UP:
        this.y--;
        break;
      case Phaser.DOWN:
        this.y++;
        break;
      case Phaser.LEFT:
        this.x--;
        break;
      case Phaser.RIGHT:
        this.x++;
        break;
      default:
        console.log("ERROR: PythonSprite.move");
    }
    this.updatePos();
  },

  updatePos: function(direction) {
    this.sprite.x = this.x * 32
    this.sprite.y = this.y * 32
  }
}

PythonWars.prototype = {

  init: function () {

  },

  preload: function () {

    this.load.tilemap('map', 'static/assets/maze.json', null, Phaser.Tilemap.TILED_JSON);
    this.load.image('tiles', 'static/img/tiles.png');
    this.load.image('bot', 'static/img/bot.png');
  },

  create: function () {
    this.map = this.add.tilemap('map');
    this.map.addTilesetImage('tiles', 'tiles');

    this.layer = this.map.createLayer('Tile Layer 1');


    this.cursors = this.input.keyboard.createCursorKeys();

    sprites = {
                "A": [1, 1],
                "B": [3, 1],
                "C": [4, 1],
                "D": [5, 1]
    };

    actions = [
                ["A", "DOWN"],
                ["A", "DOWN"],
                ["A", "DOWN"],
                ["A", "DOWN"],
                ["A", "RIGHT"],
                ["C", "RIGHT"],
                ["C", "RIGHT"],
                ["C", "LEFT"],
                ["D", "DESTRUCT"]
    ];

    this.loadSprites(sprites);
    this.run(actions);
  },

  loadMap: function(mapData) {

  },

  loadSprites: function(sprites) {
    for( var key in sprites)
    {
      x = sprites[key][0];
      y = sprites[key][1];
      sprite = this.add.sprite(32, 32, 'bot');
      this.sprites[key] = new PythonSprite(key, x, y, sprite);
      this.sprites[key].init();
    }
  },

  commands: function(id, command) {
    sprite = this.sprites[id];
    switch(command) {
        case "UP":
          sprite.move(Phaser.UP);
          break;
        case "DOWN":
          sprite.move(Phaser.DOWN);
          break;
        case "RIGHT":
          sprite.move(Phaser.RIGHT);
          break;
        case "LEFT":
          sprite.move(Phaser.LEFT);
          break;
        case "DESTRUCT":
          delete this.sprites[id];
          break;
        default:
            console.log("ERROR: invalid command ", command);
    }

  },

  run: function(actions) {
    if (actions.length > 0) {
      a = actions.shift();
      id = a[0];
      action = a[1];
      this.commands(id, action);
      setTimeout(this.run(actions), 10000);
    }
  },

  update: function () {
  },

  render: function () {

  }

};

game.state.add('Game', PythonWars, true);
