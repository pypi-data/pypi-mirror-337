from typing import Optional, List

class ObjectsData:
    def __init__(self, key: str, Name: str, DisplayName: str, Description: str, Type: str, Category: int, Price: int, 
                 Texture: Optional[str] = None, SpriteIndex: int = 0, ColorOverlayFromNextIndex: bool = False, 
                 Edibility: int = -300, IsDrink: bool = False, Buffs: Optional[List[str]] = None, 
                 GeodeDropsDefaultItems: bool = False, GeodeDrops: Optional[List[str]] = None, 
                 ArtifactSpotChances: Optional[str] = None, CanBeGivenAsGift: bool = True, 
                 CanBeTrashed: bool = True, ExcludeFromFishingCollection: bool = False, 
                 ExcludeFromShippingCollection: bool = False, ExcludeFromRandomSale: bool = False, 
                 ContextTags: Optional[List[str]] = None, CustomFields: Optional[str] = None):
        
        self.key=key
        # Atribuindo valores padrão para listas e outros mutáveis
        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description
        self.Type = Type
        self.Category = Category
        self.Price = Price
        self.Texture = Texture
        self.SpriteIndex = SpriteIndex
        self.ColorOverlayFromNextIndex = ColorOverlayFromNextIndex
        self.Edibility = Edibility
        self.IsDrink = IsDrink
        self.Buffs = Buffs if Buffs is not None else []  # Se None, usa lista vazia
        self.GeodeDropsDefaultItems = GeodeDropsDefaultItems
        self.GeodeDrops = GeodeDrops if GeodeDrops is not None else []  # Se None, usa lista vazia
        self.ArtifactSpotChances = ArtifactSpotChances
        self.CanBeGivenAsGift = CanBeGivenAsGift
        self.CanBeTrashed = CanBeTrashed
        self.ExcludeFromFishingCollection = ExcludeFromFishingCollection
        self.ExcludeFromShippingCollection = ExcludeFromShippingCollection
        self.ExcludeFromRandomSale = ExcludeFromRandomSale
        self.ContextTags = ContextTags if ContextTags is not None else []  # Se None, usa lista vazia
        self.CustomFields = CustomFields

    def getJson(self) -> dict:
        return {
            "Name": self.Name,
            "DisplayName": self.DisplayName,
            "Description": self.Description,
            "Type": self.Type,
            "Category": self.Category,
            "Price": self.Price,
            "Texture": self.Texture,
            "SpriteIndex": self.SpriteIndex,
            "ColorOverlayFromNextIndex": self.ColorOverlayFromNextIndex,
            "Edibility": self.Edibility,
            "IsDrink": self.IsDrink,
            "Buffs": self.Buffs,
            "GeodeDropsDefaultItems": self.GeodeDropsDefaultItems,
            "GeodeDrops": self.GeodeDrops,
            "ArtifactSpotChances": self.ArtifactSpotChances,
            "CanBeGivenAsGift": self.CanBeGivenAsGift,
            "CanBeTrashed": self.CanBeTrashed,
            "ExcludeFromFishingCollection": self.ExcludeFromFishingCollection,
            "ExcludeFromShippingCollection": self.ExcludeFromShippingCollection,
            "ExcludeFromRandomSale": self.ExcludeFromRandomSale,
            "ContextTags": self.ContextTags,
            "CustomFields": self.CustomFields
        }