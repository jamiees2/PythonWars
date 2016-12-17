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
    game.add.tween(this.sprite).to( { x: this.x * 32, y: this.y * 32  }, 500, Phaser.Easing.Linear.None, true );
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
    this.load.tilemap('map', '/static/assets/maze.csv', null, Phaser.Tilemap.CSV);
    this.load.image('tiles', '/static/img/tiles.png');
    this.load.spritesheet('sprites', '/static/img/sprites.png', 32, 32, 5);
  },

  create: function () {
    this.map = this.add.tilemap('map');
    this.map.addTilesetImage('tiles', 'tiles');

    layer = this.map.createLayer(0);
    layer.resizeWorld();

    this.cursors = this.input.keyboard.createCursorKeys();
  },

  loadMap: function(mapData) {
    this.load.tilemap('map', null, mapData, Phaser.Tilemap.CSV);
    this.map = this.add.tilemap('map');
    this.map.addTilesetImage('tiles', 'tiles');
    layer = this.map.createLayer(0);
    layer.resizeWorld();
  },

  loadSprite: function(id, args) {
    type = args[0]
    x = args[1]
    y = args[2]

    switch(type){
        case "PLAYER":
          sprite = this.add.sprite(32, 32, 'sprites');
          break;
        case "ENEMY":
          sprite = this.add.sprite(32, 32, 'sprites', 1);
          break;
        case "COIN":
          // coinValue = args[3];
          sprite = this.add.sprite(32, 32, 'sprites', 2);
          break;
    }

    this.sprites[id] = new PythonSprite(id, x, y, sprite);
    this.sprites[id].init();
  },

  resetSprites: function() {
    for(var id in this.sprites)
    {
      this.world.remove(this.sprites[id].sprite);
      delete this.sprites[id];
    }
  },

  commands: function(id, command, args) {
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
          this.world.remove(this.sprites[id].sprite);
          delete this.sprites[id];
          break;
        case "CREATE":
          this.loadSprite(id, args);
          break;
        default:
            console.log("ERROR: invalid command ", command);
    }

  },

  actionLoop: function(actions) {
    if (actions.length > 0) {
      a = actions.shift();

      for(tick in a) {
        tick_actions = a[tick];
        id = tick_actions.shift();
        action = tick_actions.shift();
        this.commands(id, action, tick_actions);
      }

      this.time.events.add(Phaser.Timer.SECOND * 0.7, function(){this.actionLoop(actions)}, this);
    }
  },

  run: function(actions, maze) {
    this.loadMap(maze);
    this.resetSprites();
    this.actionLoop(actions);
  },

  update: function () {
  },

  render: function () {

  }

};

game.state.add('Game', PythonWars, true);
