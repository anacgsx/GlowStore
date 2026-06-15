from decimal import Decimal
from django.core.management.base import BaseCommand
from store.models import BeautyStore, Category, GlowReward, Product


class Command(BaseCommand):
    help = 'Cria dados de exemplo da GlowStore.'

    def handle(self, *args, **options):
        categories_data = {
            'Make': 'Maquiagem para olhos, lábios, pele e acabamento glow.',
            'Skincare': 'Rotina de tratamento, hidratação e cuidado da pele.',
            'Cabelo': 'Finalizadores, tratamentos e proteção capilar.',
            'Perfume': 'Fragrâncias e body mists para a rotina.',
            'Corpo': 'Cuidados corporais, hidratação e banho.',
            'Unhas': 'Esmaltes, bases e produtos para nail care.',
        }
        categories = {}
        for name, description in categories_data.items():
            category, _ = Category.objects.update_or_create(
                name=name,
                defaults={'description': description},
            )
            categories[name] = category

        stores_data = [
            ('Ruby Rose', 'beauty with you', 'Curadoria sofisticada de maquiagem, skincare e perfumes para quem gosta de estética clean.', 'stores/logos/rubyrose.png', True),
            ('Vizzela', 'multi-tasking magic', 'Produtos práticos para durar o dia todo com uma vibe editorial e feminina.', 'stores/logos/vizzela.png', True),
            ('Rhode', 'soft science for skin', 'Skincare minimalista com foco em textura, glow e rotina simples.', 'stores/logos/rhode_logo.jpg', True),
            ('Braé', 'cabelo com acabamento de salão', 'Produtos capilares para finalizar, tratar e proteger os fios.', 'stores/logos/brae_logo.png', False),
        ]
        stores = {}
        for name, slogan, desc, logo, featured in stores_data:
            store, _ = BeautyStore.objects.update_or_create(
                name=name,
                defaults={
                    'slogan': slogan,
                    'description': desc,
                    'logo': logo,
                    'is_featured': featured,
                },
            )
            stores[name] = store

        products = [
            ('Vizzela', 'Make', 'Cherry Gloss', 'O meu cherry gloss com chaveiro possui tom vermelho cereja translúcido, textura confortável, hidratação prolongada e brilho delicado para acompanhar a rotina.', '78.90', '92.00', 'cherry', 'products/cherryGloss.png', True),
            ('Vizzela', 'Make', 'Blush Stick Red Mocha Vizzela + Las', 'Textura cremosa que desliza na pele, esfuma sem esforço e entrega efeito tint natural de longa duração.', '59.90', '69.90', 'red mocha', 'products/blush-vizzela.png', True),
            ('Vizzela', 'Make', 'Fixador de Maquiagem Real Fix', 'Fixador de maquiagem de alta performance com fitoextratos, aloe vera, chá verde e D-pantenol.', '86.90', '', 'clear', 'products/Real-Fix-01.png', True),
            ('Ruby Rose', 'Make', 'Caneta Delineadora Glass Hb524', 'Alta pigmentação, acabamento matte, secagem rápida e ponteira ultrafina para controle da aplicação.', '22.58', '', 'black', 'products/delineador.png', True),
            ('Ruby Rose', 'Make', 'Batom Líquido Obsidian OCL06', 'Textura cremosa, pigmentada e confortável, com acabamento elegante para o dia inteiro.', '23.80', '32.90', 'obsidian', 'products/batomLiquido.png', True),
            ('Ruby Rose', 'Make', 'Blush Carved in Marble Obsidian', 'Blush versátil que também pode ser usado como iluminador e sombra em uma rotina prática.', '27.17', '', 'soft floral', 'products/marble-blush.png', False),
            ('Rhode', 'Skincare', 'Glazing Milk', 'Complexo leitoso rico em nutrientes que prepara, hidrata e fortalece a barreira da pele.', '160.00', '', 'milk white', 'products/glazing-milk.png', True),
            ('Rhode', 'Make', 'Pocket Blush', 'Blush cremoso para levar na bolsa, com rubor acetinado, difuso e acabamento luminoso.', '125.00', '', 'toast', 'products/blush-rhode.png', True),
            ('Braé', 'Cabelo', 'Kit Essential Duo 1L', 'Linha de hidratação prolongada e reparação para cabelos opacos e danificados.', '150.00', '175.00', 'vanilla', 'products/kit-essential-duo.png', False),
            ('Braé', 'Cabelo', 'Essential Leave-In Fluido Reparador', 'Leave-in leve com ácido hialurônico, óleo de coco e pantenol para proteger e finalizar os fios.', '89.90', '', 'clear', 'products/leave-in.png', True),
            ('Ruby Rose', 'Make', 'Paleta de Sombras Precious Obsidian', 'Paleta com tons de preto profundo e nuances de marrom para looks diários ou dramáticos.', '78.90', '', 'rose', 'products/paleta.png', False),
            ('Rhode', 'Make', 'Peptide Lip Tint', 'Lip tint nutritivo com cor suave, brilho perolado e sensação hidratante nos lábios.', '100.00', '', 'sweet pea', 'products/peptide-lip-tint.png', False),
        ]
        product_map = {}
        for store_name, cat_name, name, desc, price, old_price, color, image, trending in products:
            product, _ = Product.objects.update_or_create(
                store=stores[store_name],
                name=name,
                defaults={
                    'category': categories[cat_name],
                    'description': desc,
                    'price': Decimal(price),
                    'old_price': Decimal(old_price) if old_price else None,
                    'color_name': color,
                    'image': image,
                    'is_trending': trending,
                    'stock': 35,
                },
            )
            product_map[name] = product

        rewards = [
            ('R$10 OFF GlowClub', 'Cupom de R$10 para usar no checkout.', 150, 'discount', '10.00', None),
            ('R$25 OFF GlowClub', 'Cupom de R$25 para uma compra especial.', 320, 'discount', '25.00', None),
            ('Mini treat surpresa', 'Resgate simbólico de um produto/mimo GlowClub.', 500, 'product', '0.00', product_map.get('Cherry Gloss')),
        ]
        for title, description, points, reward_type, discount, product in rewards:
            GlowReward.objects.update_or_create(
                title=title,
                defaults={
                    'description': description,
                    'points_required': points,
                    'reward_type': reward_type,
                    'discount_value': Decimal(discount),
                    'product': product,
                    'is_active': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('GlowStore populada com sucesso.'))
