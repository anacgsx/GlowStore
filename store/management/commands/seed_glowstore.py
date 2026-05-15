from decimal import Decimal
from django.core.management.base import BaseCommand
from store.models import BeautyStore, Category, Product


class Command(BaseCommand):
    help = 'Cria dados de exemplo da GlowStore.'

    def handle(self, *args, **options):
        categories = {}
        for name in ['Make', 'Skincare', 'Cabelo', 'Perfume', 'Corpo']:
            categories[name], _ = Category.objects.get_or_create(name=name)

        stores_data = [
            ('Ruby Rose', 'beauty with you', 'Curadoria sofisticada de maquiagem, skincare e perfumes para quem gosta de estética clean.', True),
            ('Vizzela', 'multi-tasking magic', 'Produtos práticos para durar o dia todo com uma vibe editorial e feminina.', True),
            ('Rhode', 'soft science for skin', 'Skincare minimalista com foco em textura, glow e rotina simples.', False),
            ('Braé', 'cabelo com acabamento de salão', 'Produtos capilares para finalizar, tratar e proteger os fios.', False),
        ]
        stores = {}
        for name, slogan, desc, featured in stores_data:
            stores[name], _ = BeautyStore.objects.get_or_create(
                name=name,
                defaults={'slogan': slogan, 'description': desc, 'is_featured': featured},
            )

        products = [
            ('Vizzela', 'Make', 'Cherry Gloss', 'O meu cherry gloss com chaveiro, possui um tom vermelho cereja translúcido que realça a cor natural dos lábios com leve toque avermelhado. ele entrega aquele efeito delicado perfeito com toque leve, fórmula confortável e cheirinho irresistível de cereja. sua textura cremosa não escorre, hidrata enquanto dá uma cor incrível nos lábios, e ainda pode ser usado sozinho ou por cima do batom. o resultado? lábios com aparência mais volumosa, hidratados e com a cor cherry que a gente ama, agora na versão gloss com chaveiro para te acompanhar onde você for. enriquecido com ácido hialurônico e vitamina e que irão promover hidratação prolongada e proteção aos lábios.', '78.90', 'cherry', True),
            ('Vizzela', 'Make', 'Blush Stick Red Mocha Vizzela + Las', 'Blush Stick Red MochaTextura cremosa que desliza facilmente sobre a pele, esfuma sem esforço e entrega um efeito tint natural de longa duração. Após esfumado, seca completamente, sem deixar resíduos oleosos. O blush cremoso adiciona naturalidade à maquiagem e pode ser usado também por baixo de blushes em pó para aumentar ainda mais a durabilidade. A cor Red Mocha possui um tom marrom avermelhado que se adapta perfeitamente a todos os tons de pele.', '59.90', 'red mocha', True),
            ('Vizzela', 'Make', 'Fixador de Maquiagem Real Fix', 'O Real Fix é um fixador de maquiagem de alta performance, formulado com alta concentração de resina, que proporciona maior durabilidade e resistência para a make. Sua fórmula também cuida da pele, graças à combinação de fitoextratos de alecrim, aloe vera e chá verde, que oferecem ação antioxidante e revitalizante, além do D-pantenol, que promove nutrição e hidratação.', '86.90', 'clear', True),
            ('Ruby Rose', 'Make', 'Caneta Delineadora Glass Hb524', 'Com alta pigmentação, acabamento matte e secagem rápida, a CANETA DELINEADORA GLASS desliza facilmente na pele, graças a sua ponteira ultrafina que auxilia no controle da aplicação, proporcionando um traço fino e preciso, possibilitando também as variações. ', '22.58', 'black', True),
            ('Ruby Rose', 'Make', 'Batom Liquido Obsidian Ocl06 Hb71006', 'Desfrute da combinação perfeita entre conforto e cor com o Batom Líquido Crème Lip Obsidian da Ruby Rose. Sua textura cremosa e pigmentada oferece uma aplicação suave e duradoura sem pesar nos lábios. Além de proporcionar um acabamento impecável, o batom mantém os lábios hidratados e ajuda a suavizar as linhas finas, garantindo um visual elegante o dia inteiro.', '23.80', 'clear glow', True),
            ('Ruby Rose', 'Make', 'Blush Carved In Marble Obsidian Aphrodite Of Milos Hb10021', 'O CARVED IN MARBLE BLUSH BAKED OBSIDIAN é um blush versátil que serve como blush, iluminador e sombra, perfeito para quem busca praticidade no kit de beleza. ', '27.17', 'soft floral', False),
            ('Rhode', 'Skincare', 'Glazing Milk', 'O passo essencial de preparação para sua rotina de cuidados com a pele. O Glazing Milk é um complexo potente e rico em nutrientes com uma textura leitosa que deixa a pele hidratada e radiante, ao mesmo tempo que fortalece a barreira cutânea ao longo do tempo.', '160.00', 'milk white', True),
            ('Rhode', 'Make', 'Pocket Blush', 'Um toque de blush para um toque de cor. Nosso blush cremoso para levar na bolsa ilumina as bochechas e os lábios com um rubor acetinado e difuso que se funde suavemente à pele e dura o dia todo. Sua fórmula leve hidrata a pele, deixando as bochechas macias como as de um bebê e com um acabamento luminoso, sem sensação oleosa.', '125.00', 'golden', True),
            ('Braé', 'Cabelo', 'Kit Essential Duo 1L', 'A linha Essential da BRAÉ é a solução ideal para quem busca hidratação prolongada e reparação para cabelos opacos e danificados. Especialmente formulada com ativos poderosos que oferecem proteção diária contra agressões térmicas e externas, mantendo seus fios saudáveis, macios e cheios de vida. A linha Essential é perfeita para quem quer cabelos mais hidratados e reparados.', '150.00', 'vanilla', False),
            ('Braé', 'Cabelo', 'Essential - Leave-In Fluido Reparador 260ml', 'O Essential Leave-In Fluído Reparador da BRAÉ é o cuidado perfeito para quem deseja cabelos macios, reparados e protegidos diariamente. Sua fórmula leve, enriquecida com Ácido Hialurônico, Óleo de coco  e Pantenol, repara, hidrata e protege os fios contra agressões externas e térmicas, garantindo um acabamento sedoso e saudável. Essencial para tudo, Essential para todas.', '89.90', 'clear', True),
            ('Ruby Rose', 'Make', 'Paleta De Sombras Precious Obsidian Hb2601 ', 'A paleta Precious de Obsidian realmente soa como uma adição impactante e luxuosa para qualquer coleção de maquiagem! Com tons de preto profundo e variadas nuances de marrom, essa paleta oferece uma base excelente tanto para looks diários quanto para produções mais elaboradas e dramáticas. São 18 cores que você pode ousar com várias combinações.', '78.90', 'rose', False),
            ('Rhode', 'Make', 'Peptide Lip Tint', 'Conheça o Peptide Lip Tint na cor Sweet Pea, uma edição limitada escolhida a dedo pela nossa comunidade. Sua fórmula nutritiva, com um toque de cor e brilho perolado, hidrata e revitaliza os lábios, deixando um acabamento luminoso e radiante. Tem aroma de frutas vermelhas frescas e jasmim.', '100.00', 'glow red', False),
        ]
        for store_name, cat_name, name, desc, price, color, trending in products:
            Product.objects.get_or_create(
                store=stores[store_name],
                name=name,
                defaults={
                    'category': categories[cat_name],
                    'description': desc,
                    'price': Decimal(price),
                    'color_name': color,
                    'is_trending': trending,
                    'stock': 35,
                },
            )
        self.stdout.write(self.style.SUCCESS('GlowStore populada com sucesso.'))
