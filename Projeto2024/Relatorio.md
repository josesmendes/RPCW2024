# Elden of the Rings

## Introdução
No âmbito da disciplina de Representação e Processamento de Conhecimento Web criamos uma ontologia baseada no jogo "Elden Ring". Para o efeito, foram utilizados datasets encontrados na plataforma Kaggle. 
Os dataset incluia ficheiros para os seguintes dados sorceries, items, bosses, incantations, locations, spirits, talismans, shields, creatures, classes, ashes, armors, ammos, npcs and weapons. 


## Explicação dos datasets
Tal como foi dito anteriormente este dateset vinha dividido nos seguintes ficheiros:
- sorceries, 
- items, 
- bosses, 
- incantations,
- locations,
- spirits,
- talismans,
- shields,
- creatures,
- classes,
- ashes,
- armors,
- ammos,
- npcs,
- weapons.
que irão compor a maioria das classes criadas na ontologia(que irá ser explicada posteriormente).
Os datasets presentes no Kaggle encontravam-se em algumas amostras com os  valores em falta ou com informação errada, como por exemplo "crystal tears" e não "crystal tear", assim como certas entradas onde eram descritos os valores de dano e defesa dos objetos estarem, incompletas/mal-formatas. Para tal, foi preciso fazer uma análise cuidada de todos os datasets e completar as amostras analisando o jogo original ou, então, apagar linhas onde essa informação não era diponibilizada no site oficial de "Elden Ring".
Foram também analisadas as colunas dos diferentes datasets e algumas que não eram consideradas importantes para a nossa ontologia foram apagadas, como é exemplo, a coluna types no dataset incantations que apenas continha palavras como Incantation ou Incantations. 


## Ontologia
Na criação da ontologia foram criadas diversas classes, subclasses, data properties e object properties. 
Esta ontologia deve responder a perguntas como: "Quais são os itens disponiveis no jogo?", "A que região pertence cada localização?", "Quais são os bosses que podemos encontrar em cada região?", "Onde podem ser encontradas determinadas criaturas?" "Que items são recebidos depois de derrotar um boss" e que "items são encontrados depois de derrotar um boss".

A ontologia será utilizada por desenvolvedores de jogos, pesquisadores em estudos de jogos, e entusiastas que desejam aprofundar seu conhecimento sobre "Elden Ring". 


### Classes e Subclasses
As classes representam categorias amplas de entidades, enquanto as subclasses são agrupamentos mais específicos dentro dessas categorias. Na ontologia de "Elden Ring", temos várias classes, como Ammos, que representa tipos de munição usados no jogo; Armors, que cobre todos os tipos de equipamentos de proteção; Ashes, que se refere a itens relacionados à invocação de espíritos; Bosses, que inclui todos os principais adversários que os jogadores encontram; e Classes, que são as diferentes classes de personagens que os jogadores podem escolher. Dentro de Classes, temos subclasses como Astrologer, Bandit, Confessor,  Hero, Prisoner, Prophet, Samurai,  Vagabond, Warrior e Wretch.

Outras classes incluem Creatures, que engloba diversos inimigos; Incantations, que representa feitiços e habilidades mágicas;
Items, uma categoria geral para todos os itens utilizáveis no jogo, com subclasses como Consumable, itens que podem ser usados uma vez; Crystal_Tear, itens usados para buffs específicos ou habilidades; Info_Item, itens que fornecem informações; Key_Item, itens importantes necessários para a progressão do jogo; Misc, diversos itens variados; e Reusable, itens que podem ser usados várias vezes.
Há também Npcs, personagens não-jogáveis no jogo; 
Region, áreas geográficas dentro do mundo do jogo;
Shields, equipamentos defensivos com subclasses como Greatshield, Medium_Shield  e Small_Shield. 
Além disso, temos Sorceries, feitiços mágicos de um tipo específico; Spirits, entidades invocáveis que ajudam o jogador; 
Talismans, itens que concedem bônus passivos; 
Weapons, equipamentos ofensivos com inúmeras subclasses, incluindo Axe, Ballista, Bow, Claw,  Colossal_Sword, Colossal_Weapon;
Crossbow, Curved_Greatsword, Curved_Sword, Dagger, Fist, Flail,  Glintstone_Staff, Greataxe, grandes machados; Greatbow entre outros. 


### Propriedades de Objeto
As propriedades de objeto definem as relações entre diferentes entidades. A propriedade "bossDrops" especifica os itens que os chefes deixam cair ao serem derrotados, com seu domínio em Bosses e seu alcance incluindo Armors, Ashes, Incantations, Items, Shields, Sorceries, Spirits, Talismans e Weapons. A propriedade "creatureDropsItem" especifica itens deixados por criaturas, com seu domínio em Creatures e seu alcance em Items. A propriedade isInLocation indica a localização de chefes, criaturas e NPCs, com seu domínio incluindo Bosses, Creatures e Npcs, e seu alcance em Location. A propriedade "isInRegion" especifica a região de chefes, criaturas, locais e NPCs, com seu domínio incluindo Bosses, Creatures, Location e Npcs, e seu alcance em Region.


### Propriedades de Dados 
As propriedades de dados definem os atributos e características das entidades. A propriedade affinity aplica-se a Ashes, definindo seu alinhamento elemental ou mágico. A propriedade damageNegation é usada para Armors, indicando quanto dano elas podem negar. A propriedade damageType descreve o tipo de dano para Ammos, Shields e Weapons. A propriedade defenceType especifica o tipo de defesa para Armors, Shields e Weapons. A propriedade description fornece uma descrição textual para entidades todas as entidades da nossa ontologia, de maneira a facilitar a transmissão de informação que os outros dados não sejam capazes de fornecer. A propriedade effect descreve os efeitos de Incantations, Items, Sorceries, Spirits e Talismans. A propriedade fpCost indica o custo em pontos de foco para Incantations, Sorceries e Spirits, que pode ou não exister(apenas no caso dos Spirits). A propriedade healthPoints aplica-se a Bosses, especificando seus pontos de vida. A propriedade hpCost especifica o custo em pontos de vida para Spirits, que pode ou não existir. A propriedade image liga a uma imagem para várias entidades, incluindo Ammos, Armors, Ashes, Bosses, Classes, Creatures, Incantations, Items, Npcs, Region, Shields, Sorceries, Spirits, Talismans e Weapons. A propriedade passive descreve os efeitos passivos para Ammos. A propriedade quote contém citações para Npcs. A propriedade requiresAttributes especifica atributos necessários para Incantations, Shields, Sorceries e Weapons. A propriedade resistance indica valores de resistência para Armors. A propriedade role define o papel de Npcs. A propriedade scalesWith indica com quais atributos as armas ou escudos escalam para Shields e Weapons. A propriedade skill descreve habilidades associadas com Ashes. A propriedade slots indica o número de slots usados por Incantations e Sorceries. A propriedade weight especifica o peso de Armors, Shields e Weapons.


## Criação da App
A aplicação desenvolvida é uma plataforma web interativa que permite aos usuários explorar dados detalhados do jogo Elden Ring. Utilizando uma interface amigável, a aplicação possibilita a navegação através de várias categorias de informações, como armas, itens, localizações, regiões, NPCs, entre outras. Cada categoria é apresentada em listas organizadas, e ao clicar num item específico, o usuário é direcionado a uma página detalhada contendo informações enriquecidas, incluindo imagens e descrições detalhadas.


#### Funcionalidades 
##### Página Inicial:
 A página inicial oferece links para todas as categorias principais, permitindo fácil navegação.
Exploração de Itens: Os itens são categorizados por subclasses. Cada subclasse lista todos os itens correspondentes com seus respectivos nomes e imagens.
##### Detalhes dos Itens:
 Ao clicar num item, o usuário pode ver uma descrição detalhada do item, seus efeitos, requisitos e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Regiões:
 As regiões do jogo são listadas, e ao selecionar uma região, o usuário pode ver todas as localizações e "Bosses" presentes naquela região.
Detalhes das Localizações: Incluem descrições, imagens e links para regiões relacionadas.
##### Exploração de NPCs:
 Lista de NPCs com imagens e descrições detalhadas sobre seu papel no jogo e sua localização.
##### Exploração de Armas:
 As armas são categorizados por tipos. Cada tipo lista todas as armas correspondentes com seus respectivos nomes e imagens.
##### Detalhes dos Armas:
 Ao clicar numa arma, o usuário pode ver uma descrição detalhada da arma, seus requisitos, estatisticas e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Escudos:
 Os escudos são categorizados por tipos. Cada tipo lista todos os escudos correspondentes com seus respectivos nomes e imagens.
##### Detalhes dos Escudos:
 Ao clicar num escudo, o usuário pode ver uma descrição detalhada do escudo, seus requisitos, estatisticas e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Incantações:
 As incantações do jogo são listadas, e ao selecionar uma incantações, o usuário pode ver uma descrição detalhada do escudo, seus requisitos, estatisticas e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Feitiços:
 Os feitiços do jogo são listadas, e ao selecionar um feitiço, o usuário pode ver uma descrição detalhada do feitiço, seus requisitos, estatisticas e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Armaduras:
 as armaduras são categorizados por tipos. Cada tipo lista todas as armaduras correspondentes com seus respectivos nomes e imagens.
##### Detalhes dos Armaduras:
 Ao clicar numa armadura, o usuário pode ver uma descrição detalhada da armadura, estatisticas e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Cinzas:
 As cinzas do jogo são listadas, e ao selecionar uma cinza, o usuário pode ver uma descrição detalhada da cinza, a habilidade a esta associada, a sua afinidade e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Talismans:
 Os talismans do jogo são listadas, e ao selecionar um talisman, o usuário pode ver uma descrição detalhada do talisman, seus efeitos e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Espiritos:
 Os espiritos do jogo são listadas, e ao selecionar um espiritos, o usuário pode ver uma descrição detalhada do espiritos, seus requisitos(pontos de vida, foco ou nenhum), efeito e , em caso de haver, o boss que necessita de ser derrotado de forma a a obter.
##### Exploração de Classes:
 As classes do jogo são listadas, e ao selecionar uma classe, o usuário pode ver uma descrição detalhada da classe, atributos, arma, escudo e armas iniciais.
 ##### Exploração de Munições:
 As munições do jogo são listadas, e ao selecionar uma munições, o usuário pode ver uma descrição detalhada da munições, atributos e passiva, caso a tenha.
##### Adição de novas entradas na ontologia: 
 É possível, através de um butão na pagina inicial, selecionar o tipo de nova entidade a adicionar. As opções são as classes enumeradas previamente, Items, Region, Location, Npc, Weapon, Shield, Armor, Talisman, Ashes, Spirits, Classes, Bosses e Ammos.
 Após selecionado o tipo o utilizador é dirigido para uma página que contem os campos necessários, e opcionais, que tem de ser preenchidos para a adição correta daquele elemento na ontologi
##### Remoção de uma entrada da ontologio:
 É possível na pagina de cada entrada removê-la da ontologia através de um butão. Após premir este butão a entrada é removida e o utilizador é reencaminhado para a página do tipo do elemento acabado de remover.



#### Desenvolvimento 
A aplicação foi desenvolvida utilizando o framework Flask para a criação de aplicações web em Python. Flask foi configurado para definir rotas que respondem a diferentes URLs, facilitando a navegação entre diferentes seções da aplicação. Para a persistência e recuperação dos dados, foi utilizado o GraphDB, um banco de dados RDF que permite consultas SPARQL para manipulação de dados semânticos. Consultas SPARQL foram escritas para extrair dados RDF do GraphDB, e essas consultas foram integradas nas rotas Flask para buscar informações dinâmicas de acordo com a necessidade do usuário.

Para a renderização das páginas web, foram utilizados templates Jinja2. Esses templates permitem a inserção dinâmica de dados nos HTMLs. A interface foi criada usando CSS, com o framework W3.CSS, garantindo um design limpo e responsivo.


## Conclusão
A aplicação oferece uma plataforma robusta para explorar informações detalhadas sobre o jogo Elden Ring, utilizando tecnologias modernas de desenvolvimento web e bancos de dados semânticos. A estrutura modular do código facilita futuras expansões e manutenção, garantindo que a aplicação permaneça útil e relevante conforme novos dados, ligações ou funcionalidades sejam adicionados.
